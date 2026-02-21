from unicodedata import east_asian_width, category

class Element(str):
    def get_gap_previous(self, previous_element: 'Element') -> int:
        return 0
    
    def get_gap_next(self, next_element: 'Element') -> int:
        return 0
    
    def __repr__(self):
        return f"{self.__class__.__name__}({super().__repr__()})"

class Word(Element):
    pass

class CJKWord(Element):
    def get_gap_previous(self, previous_element: 'Element') -> int:
        return 1 if isinstance(previous_element, Word) else 0
    
    def get_gap_next(self, next_element: 'Element') -> int:
        return 1 if isinstance(next_element, Word) else 0

class Punctuation(Element):
    pass

class CJKPunctuation(Element):
    pass

class Space(Element):
    pass

def is_space(char: str):
    if len(char) != 1:
        raise ValueError("Input must be a single character")
    return char.isspace()

def is_cjk(char: str):
    if len(char) != 1:
        raise ValueError("Input must be a single character")
    ea = east_asian_width(char)
    return ea in ('F', 'W')

def is_punctuation(char: str):
    if len(char) != 1:
        raise ValueError("Input must be a single character")
    return category(char).startswith('P')

def parse(text: str) -> list[Element]:
    """
    Split text into `Word`, `CJKWord`, `Punctuation`, `CJKPunctuation`, and `Space` elements.
    """
    if not text:
        return []
    
    result = []
    current_segment = ''
    current_type = None
    
    for ch in text:
        if is_space(ch):
            typ = Space
        elif is_cjk(ch):
            if is_punctuation(ch):
                typ = CJKPunctuation
            else:
                typ = CJKWord
        else:
            if is_punctuation(ch):
                typ = Punctuation
            else:
                typ = Word
        if typ in (CJKWord, CJKPunctuation):
            # CJK characters are always a single segment
            if current_segment:
                result.append(current_type(current_segment))  # type: ignore
                current_segment = ''
                current_type = None
            result.append(typ(ch))
        else:
            # Non-CJK
            if typ == current_type:
                current_segment += ch
            else:
                if current_segment:
                    result.append(current_type(current_segment))  # type: ignore
                current_segment = ch
                current_type = typ

    if current_segment:
        result.append(current_segment)
    
    return result