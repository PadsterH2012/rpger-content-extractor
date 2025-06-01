#!/usr/bin/env python3
"""
Text Quality Enhancement Module
Provides spell checking, OCR artifact cleanup, and quality scoring for extracted PDF text
"""

import re
import logging
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import json
from pathlib import Path

try:
    from spellchecker import SpellChecker
    SPELLCHECKER_AVAILABLE = True
except ImportError:
    SPELLCHECKER_AVAILABLE = False

try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False

try:
    import nltk
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False

@dataclass
class QualityMetrics:
    """Quality assessment metrics for text"""
    overall_score: float
    spelling_score: float
    character_cleanup_score: float
    readability_score: float
    word_count: int
    corrected_words: int
    cleaned_characters: int
    issues_found: List[str]
    grade: str  # A-F grade

@dataclass
class TextCleanupResult:
    """Result of text cleanup process"""
    original_text: str
    cleaned_text: str
    before_metrics: QualityMetrics
    after_metrics: QualityMetrics
    corrections_made: List[Dict[str, str]]
    cleanup_summary: Dict[str, Any]

class TextQualityEnhancer:
    """Enhanced text quality processor with spell checking and cleanup"""

    def __init__(self, config: Optional[Dict] = None):
        self.logger = logging.getLogger(__name__)
        self.config = config or {}

        # Initialize spell checker
        self.spell_checker = None
        self.textblob_available = TEXTBLOB_AVAILABLE

        if SPELLCHECKER_AVAILABLE:
            self.spell_checker = SpellChecker()
            self._load_rpg_dictionary()
        else:
            self.logger.warning("pyspellchecker not available - spell checking disabled")

        # OCR artifact patterns
        self.ocr_patterns = self._build_ocr_cleanup_patterns()

        # RPG-specific patterns
        self.rpg_patterns = self._build_rpg_patterns()

    def _load_rpg_dictionary(self):
        """Load RPG-specific terms into spell checker"""
        rpg_terms = [
            # D&D Core Terms
            'thac0', 'armor', 'armour', 'dexterity', 'charisma', 'constitution',
            'intelligence', 'wisdom', 'strength', 'hitpoints', 'hitdice',
            'dungeon', 'master', 'player', 'character', 'paladin', 'ranger',
            'cleric', 'fighter', 'magic', 'user', 'thief', 'assassin', 'monk',
            'barbarian', 'druid', 'illusionist', 'bard',

            # Spells & Magic
            'cantrip', 'cantrips', 'spell', 'spells', 'magic', 'missile',
            'fireball', 'lightning', 'bolt', 'healing', 'cure', 'wounds',
            'teleport', 'dimension', 'door', 'polymorph', 'charm', 'person',
            'sleep', 'hold', 'dispel', 'detect', 'invisibility', 'levitate',

            # Monsters & Creatures
            'orc', 'orcs', 'goblin', 'goblins', 'kobold', 'kobolds',
            'troll', 'trolls', 'ogre', 'ogres', 'giant', 'giants',
            'dragon', 'dragons', 'wyvern', 'basilisk', 'medusa',
            'lich', 'zombie', 'zombies', 'skeleton', 'skeletons',
            'vampire', 'vampires', 'werewolf', 'werewolves',

            # Equipment & Items
            'longsword', 'shortsword', 'broadsword', 'scimitar',
            'mace', 'flail', 'halberd', 'crossbow', 'longbow',
            'chainmail', 'platemail', 'leather', 'studded',
            'shield', 'buckler', 'potion', 'potions', 'scroll', 'scrolls',

            # Game Mechanics
            'saving', 'throw', 'initiative', 'melee', 'ranged',
            'damage', 'bonus', 'penalty', 'modifier', 'dice', 'roll',
            'experience', 'points', 'level', 'levels', 'advancement',

            # Locations & Settings
            'tavern', 'inn', 'castle', 'fortress', 'dungeon', 'cavern',
            'forest', 'wilderness', 'city', 'town', 'village', 'hamlet'
        ]

        # Add terms to spell checker
        if self.spell_checker:
            for term in rpg_terms:
                self.spell_checker.word_frequency.load_words([term])
                # Also add capitalized versions
                self.spell_checker.word_frequency.load_words([term.capitalize()])

    def _build_ocr_cleanup_patterns(self) -> List[Tuple[str, str]]:
        """Build patterns for cleaning OCR artifacts"""
        return [
            # Common OCR character substitutions
            (r'\b0\b', 'O'),  # Zero to O in words
            (r'\bl\b', 'I'),  # lowercase l to I
            (r'rn', 'm'),     # rn to m
            (r'cl', 'd'),     # cl to d
            (r'li', 'h'),     # li to h

            # Spacing issues (preserve line structure)
            (r'[ \t]+', ' '),    # Multiple spaces/tabs to single space (preserve newlines)
            # Join spaced letters within words - target OCR artifacts specifically
            (r'([a-zA-Z]{2,})\s+([IlL]{1,2})\b', r'\1\2'),  # Join words ending with spaced I/l/L (common OCR)
            (r'\b([a-zA-Z])\s+([a-zA-Z])\s+([a-zA-Z])\b(?=\s|$|\.)', r'\1\2\3'),  # 3 single letters forming a word
            (r'\b([a-zA-Z])\s+([a-zA-Z])\b(?=\s|$|\.)', r'\1\2'),  # 2 single letters at word end
            (r'([A-Z])\s+([A-Z])', r'\1\2'),  # Remove spaces in acronyms

            # Special characters
            (r'[\u201c\u201d\u201e]', '"'),  # Smart quotes to regular
            (r'[\u2018\u2019\u201a]', "'"),  # Smart apostrophes
            (r'—', '-'),      # Em dash to hyphen
            (r'–', '-'),      # En dash to hyphen

            # Line break artifacts (preserve paragraph structure)
            (r'-\s*\n\s*', ''),  # Hyphenated line breaks
            (r'\n\s*\n\s*\n+', '\n\n'),  # Multiple line breaks to double
        ]

    def _build_rpg_patterns(self) -> List[Tuple[str, str]]:
        """Build RPG-specific cleanup patterns"""
        return [
            # Common RPG abbreviations
            (r'\bAC\b', 'Armor Class'),
            (r'\bHP\b', 'Hit Points'),
            (r'\bHD\b', 'Hit Dice'),
            (r'\bXP\b', 'Experience Points'),
            (r'\bDM\b', 'Dungeon Master'),
            (r'\bPC\b', 'Player Character'),
            (r'\bNPC\b', 'Non-Player Character'),

            # Dice notation cleanup
            (r'(\d+)\s*d\s*(\d+)', r'\1d\2'),  # Fix spaced dice notation
            (r'(\d+)\s*D\s*(\d+)', r'\1d\2'),  # Lowercase d in dice
        ]

    def enhance_text_quality(self, text: str, aggressive: bool = False) -> TextCleanupResult:
        """
        Main method to enhance text quality with cleanup and spell checking

        Args:
            text: Original text to enhance
            aggressive: Whether to apply aggressive corrections

        Returns:
            TextCleanupResult with before/after metrics and cleaned text
        """
        self.logger.info(f"Enhancing text quality (aggressive={aggressive})")

        # Assess original quality
        before_metrics = self._assess_text_quality(text)

        # Stage 1: OCR Artifact Cleanup
        stage1_text = self._clean_ocr_artifacts(text)

        # Stage 2: RPG-specific cleanup
        stage2_text = self._apply_rpg_patterns(stage1_text)

        # Stage 3: Spell checking
        stage3_text, corrections = self._spell_check_text(stage2_text, aggressive)

        # Stage 4: Final cleanup
        final_text = self._final_cleanup(stage3_text)

        # Assess final quality
        after_metrics = self._assess_text_quality(final_text)

        # Build cleanup summary
        cleanup_summary = {
            'stages_applied': ['ocr_cleanup', 'rpg_patterns', 'spell_check', 'final_cleanup'],
            'character_changes': len(text) - len(final_text),
            'word_changes': len(text.split()) - len(final_text.split()),
            'quality_improvement': after_metrics.overall_score - before_metrics.overall_score,
            'aggressive_mode': aggressive
        }

        return TextCleanupResult(
            original_text=text,
            cleaned_text=final_text,
            before_metrics=before_metrics,
            after_metrics=after_metrics,
            corrections_made=corrections,
            cleanup_summary=cleanup_summary
        )

    def _clean_ocr_artifacts(self, text: str) -> str:
        """Clean common OCR artifacts"""
        cleaned = text

        for pattern, replacement in self.ocr_patterns:
            cleaned = re.sub(pattern, replacement, cleaned)

        return cleaned

    def _apply_rpg_patterns(self, text: str) -> str:
        """Apply RPG-specific cleanup patterns"""
        cleaned = text

        for pattern, replacement in self.rpg_patterns:
            cleaned = re.sub(pattern, replacement, cleaned)

        return cleaned

    def _spell_check_text(self, text: str, aggressive: bool = False) -> Tuple[str, List[Dict[str, str]]]:
        """Perform spell checking and correction"""
        if not self.spell_checker:
            return text, []

        corrections = []
        
        # Use regex to find words while preserving whitespace
        def replace_word(match):
            word = match.group(0)
            # Clean word for checking (remove punctuation)
            clean_word = re.sub(r'[^\w]', '', word.lower())

            if clean_word and clean_word not in self.spell_checker:
                # Get suggestions
                candidates = self.spell_checker.candidates(clean_word)
                suggestions = list(candidates) if candidates else []

                if suggestions:
                    best_suggestion = suggestions[0]

                    # Apply correction based on aggressiveness
                    if aggressive or self._should_correct(clean_word, best_suggestion):
                        # Preserve original case and punctuation
                        corrected_word = self._preserve_case_punctuation(word, best_suggestion)

                        corrections.append({
                            'original': word,
                            'corrected': corrected_word,
                            'confidence': self._correction_confidence(clean_word, best_suggestion)
                        })
                        return corrected_word

            return word

        # Replace words while preserving whitespace
        corrected_text = re.sub(r'\b\w+\b', replace_word, text)
        
        return corrected_text, corrections

    def _should_correct(self, original: str, suggestion: str) -> bool:
        """Determine if a correction should be applied"""
        # Only correct if suggestion is significantly better
        if len(original) < 3:
            return False

        # Calculate edit distance
        edit_distance = self._levenshtein_distance(original, suggestion)

        # Only correct if edit distance is small relative to word length
        return edit_distance <= max(1, len(original) // 3)

    def _levenshtein_distance(self, s1: str, s2: str) -> int:
        """Calculate Levenshtein distance between two strings"""
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = list(range(len(s2) + 1))
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    def _preserve_case_punctuation(self, original: str, corrected: str) -> str:
        """Preserve original case and punctuation in corrected word"""
        # Extract punctuation
        leading_punct = re.match(r'^[^\w]*', original).group()
        trailing_punct = re.search(r'[^\w]*$', original).group()

        # Apply case pattern
        if original.isupper():
            corrected = corrected.upper()
        elif original.istitle():
            corrected = corrected.capitalize()
        elif original.islower():
            corrected = corrected.lower()

        return leading_punct + corrected + trailing_punct

    def _correction_confidence(self, original: str, corrected: str) -> float:
        """Calculate confidence score for a correction"""
        edit_distance = self._levenshtein_distance(original, corrected)
        max_length = max(len(original), len(corrected))

        if max_length == 0:
            return 1.0

        return 1.0 - (edit_distance / max_length)

    def _final_cleanup(self, text: str) -> str:
        """Final text cleanup pass with intelligent newline handling"""
        # Stage 1: Smart newline replacement
        text = self._smart_newline_cleanup(text)

        # Stage 2: Clean up excessive whitespace (but preserve newlines)
        # Replace multiple spaces with single space, but keep newlines
        text = re.sub(r'[ \t]+', ' ', text)  # Only collapse spaces and tabs
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)  # Collapse multiple newlines to double

        # Stage 3: Clean up punctuation (but preserve line structure)
        text = re.sub(r'\s+([,.!?;:])', r'\1', text)
        # Only fix spacing within lines, not across newlines
        text = re.sub(r'([.!?])[ \t]+([A-Z])', r'\1 \2', text)

        return text.strip()

    def _smart_newline_cleanup(self, text: str) -> str:
        """Intelligently handle newlines to maintain readability"""
        # Split into lines for analysis
        lines = text.split('\n')
        processed_lines = []

        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            if not line:  # Empty line - preserve for paragraph breaks
                processed_lines.append('')
                i += 1
                continue

            # Always preserve lines that look like structural elements (headings, chapters)
            if self._is_structural_line(line):
                processed_lines.append(line)
                i += 1
                continue

            # For non-structural lines, only join if they are NOT separated by empty lines
            # Check if there's an empty line before next content line
            next_content_idx = i + 1
            while next_content_idx < len(lines) and not lines[next_content_idx].strip():
                next_content_idx += 1
                
            # If there's an empty line between current and next content, don't join
            if next_content_idx > i + 1:
                # Add period if line doesn't end with punctuation
                if line and not line.endswith(('.', '!', '?', ':', ';', ',', '-', '—', '–')):
                    processed_lines.append(line + '.')
                else:
                    processed_lines.append(line)
                i += 1
                continue
                
            # For lines not separated by empty lines, be more conservative about joining
            if next_content_idx < len(lines):
                next_line = lines[next_content_idx].strip()
                
                # Don't join if current line ends with sentence-ending punctuation
                if line.endswith(('.', '!', '?', ':', ';')):
                    processed_lines.append(line)
                    i += 1
                    continue

                # Don't join if next line starts with capital (new sentence/paragraph)
                if next_line and next_line[0].isupper():
                    if not line.endswith((',', '-', '—', '–')):
                        processed_lines.append(line + '.')
                    else:
                        processed_lines.append(line)
                    i += 1
                    continue

                # Don't join if next line is structural
                if self._is_structural_line(next_line):
                    if not line.endswith(('.', '!', '?', ':', ';', ',', '-', '—', '–')):
                        processed_lines.append(line + '.')
                    else:
                        processed_lines.append(line)
                    i += 1
                    continue

            # Default: keep line as is
            if line and not line.endswith(('.', '!', '?', ':', ';', ',', '-', '—', '–')):
                processed_lines.append(line + '.')
            else:
                processed_lines.append(line)
            i += 1

        return '\n'.join(processed_lines)

    def _is_structural_line(self, line: str) -> bool:
        """Check if a line represents structural text like headings"""
        line = line.strip()
        if not line:
            return False
        
        # Check for chapter/section patterns
        if re.match(r'^(Chapter|Section|Part|Appendix)\s+\d+', line, re.IGNORECASE):
            return True
        
        # Check for short lines that might be headings (but not single words)
        words = line.split()
        if len(words) >= 2 and len(words) <= 5 and line.endswith(':'):
            return True
            
        return False

    def _assess_text_quality(self, text: str) -> QualityMetrics:
        """Assess overall text quality and provide metrics"""
        if not text.strip():
            return QualityMetrics(
                overall_score=0.0,
                spelling_score=0.0,
                character_cleanup_score=0.0,
                readability_score=0.0,
                word_count=0,
                corrected_words=0,
                cleaned_characters=0,
                issues_found=["Empty text"],
                grade="F"
            )

        # Calculate individual scores
        spelling_score = self._calculate_spelling_score(text)
        character_score = self._calculate_character_score(text)
        readability_score = self._calculate_readability_score(text)

        # Weight the scores
        overall_score = (
            spelling_score * 0.4 +
            character_score * 0.3 +
            readability_score * 0.3
        )

        # Identify issues
        issues = self._identify_text_issues(text)

        # Calculate grade
        grade = self._score_to_grade(overall_score)

        return QualityMetrics(
            overall_score=overall_score,
            spelling_score=spelling_score,
            character_cleanup_score=character_score,
            readability_score=readability_score,
            word_count=len(text.split()),
            corrected_words=0,  # Will be updated during correction
            cleaned_characters=0,  # Will be updated during cleanup
            issues_found=issues,
            grade=grade
        )

    def _calculate_spelling_score(self, text: str) -> float:
        """Calculate spelling accuracy score"""
        if not self.spell_checker:
            return 85.0  # Default score when spell checker unavailable

        words = [re.sub(r'[^\w]', '', word.lower()) for word in text.split()]
        words = [w for w in words if w and len(w) > 1]

        if not words:
            return 100.0

        misspelled = self.spell_checker.unknown(words)
        correct_words = len(words) - len(misspelled)

        return (correct_words / len(words)) * 100

    def _calculate_character_score(self, text: str) -> float:
        """Calculate character quality score (OCR artifacts, etc.)"""
        issues = 0
        total_chars = len(text)

        if total_chars == 0:
            return 100.0

        # Check for common OCR artifacts
        ocr_artifacts = [
            r'\b0\b(?![0-9])',  # Standalone zeros (likely O)
            r'\bl\b(?![a-z])',  # Standalone l (likely I)
            r'rn(?=[a-z])',     # rn that should be m
            r'[\u201c\u201d\u201e]',  # Smart quotes
            r'[\u2018\u2019\u201a]',  # Smart apostrophes
            r'\s{2,}',          # Multiple spaces
            r'([a-z])\s+([a-z])',  # Spaced letters within words
        ]

        for pattern in ocr_artifacts:
            matches = re.findall(pattern, text)
            issues += len(matches)

        # Calculate score - use a more reasonable penalty rate
        error_rate = issues / total_chars
        return max(0, (1 - error_rate * 2) * 100)  # More balanced penalty for artifacts

    def _calculate_readability_score(self, text: str) -> float:
        """Calculate readability score based on structure"""
        if not text.strip():
            return 0.0

        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if not sentences:
            return 50.0

        words = text.split()

        # Basic readability metrics
        avg_sentence_length = len(words) / len(sentences)

        # Ideal sentence length is 15-20 words
        if 10 <= avg_sentence_length <= 25:
            length_score = 100
        elif 5 <= avg_sentence_length <= 35:
            length_score = 80
        else:
            length_score = 60

        # Check for proper capitalization
        capitalized_sentences = sum(1 for s in sentences if s and s[0].isupper())
        capitalization_score = (capitalized_sentences / len(sentences)) * 100

        # Check for proper punctuation
        punctuation_score = 100  # Assume good by default

        return (length_score + capitalization_score + punctuation_score) / 3

    def _identify_text_issues(self, text: str) -> List[str]:
        """Identify specific issues in the text"""
        issues = []

        # Check for common problems
        if re.search(r'\s{3,}', text):
            issues.append("Excessive whitespace detected")

        if re.search(r'([a-z])\s+([a-z])', text):
            issues.append("Spaced letters within words (OCR artifact)")

        if re.search(r'[\u201c\u201d\u201e]', text) or re.search(r'[\u2018\u2019\u201a]', text):
            issues.append("Smart quotes/apostrophes detected")

        if self.spell_checker:
            words = [re.sub(r'[^\w]', '', word.lower()) for word in text.split()]
            words = [w for w in words if w and len(w) > 2]
            misspelled = self.spell_checker.unknown(words)

            if len(misspelled) > len(words) * 0.1:  # More than 10% misspelled
                issues.append(f"High spelling error rate: {len(misspelled)} misspelled words")

        # Check for very short or very long sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        for sentence in sentences:
            words_in_sentence = len(sentence.split())
            if words_in_sentence > 50:
                issues.append("Very long sentences detected (may affect readability)")
                break
            elif words_in_sentence < 3 and len(sentences) > 5:
                issues.append("Very short sentences detected")
                break

        return issues

    def _score_to_grade(self, score: float) -> str:
        """Convert numeric score to letter grade"""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"

    def get_quality_summary(self, result: TextCleanupResult) -> Dict[str, Any]:
        """Generate a comprehensive quality summary"""
        improvement = result.after_metrics.overall_score - result.before_metrics.overall_score

        return {
            "before": {
                "score": round(result.before_metrics.overall_score, 1),
                "grade": result.before_metrics.grade,
                "issues": len(result.before_metrics.issues_found)
            },
            "after": {
                "score": round(result.after_metrics.overall_score, 1),
                "grade": result.after_metrics.grade,
                "issues": len(result.after_metrics.issues_found)
            },
            "improvement": {
                "score_change": round(improvement, 1),
                "grade_change": f"{result.before_metrics.grade} → {result.after_metrics.grade}",
                "corrections_made": len(result.corrections_made),
                "character_changes": result.cleanup_summary.get('character_changes', 0)
            },
            "details": {
                "word_count": result.after_metrics.word_count,
                "spelling_improvement": round(
                    result.after_metrics.spelling_score - result.before_metrics.spelling_score, 1
                ),
                "character_improvement": round(
                    result.after_metrics.character_cleanup_score - result.before_metrics.character_cleanup_score, 1
                ),
                "readability_improvement": round(
                    result.after_metrics.readability_score - result.before_metrics.readability_score, 1
                )
            }
        }
