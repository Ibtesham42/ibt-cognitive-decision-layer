"""
Universal Symbolic Language Parser - Phase 1

Converts natural language into structured symbolic representations
supporting entities, actions, relations, attributes, temporal, spatial,
causal, modal, quantifier, negation, and conditional elements.
"""

import re
import json
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Symbol:
    """Represents a single symbolic token"""
    type: str
    value: str
    original: str
    confidence: float
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class SymbolicExpression:
    """Complete symbolic representation of an input"""
    id: str
    input_text: str
    symbols: List[Symbol]
    structure: Dict[str, Any]
    ontology_map: Dict[str, str]
    timestamp: str
    processing_time_ms: float
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'input_text': self.input_text,
            'symbols': [s.to_dict() for s in self.symbols],
            'structure': self.structure,
            'ontology_map': self.ontology_map,
            'timestamp': self.timestamp,
            'processing_time_ms': self.processing_time_ms
        }
    
    def to_string(self) -> str:
        """Convert to readable symbolic string"""
        parts = []
        for sym in self.symbols:
            parts.append(f"[{sym.type}:{sym.value}]")
        return " ".join(parts)


class UniversalOntology:
    """Universal ontology covering all domains"""
    
    ENTITIES = {
        # Physical objects
        'object', 'device', 'machine', 'vehicle', 'building', 'room',
        'person', 'animal', 'plant', 'material', 'substance',
        # Abstract concepts
        'idea', 'concept', 'theory', 'principle', 'law', 'rule',
        'emotion', 'feeling', 'thought', 'belief', 'opinion',
        # Systems
        'system', 'process', 'procedure', 'method', 'algorithm',
        'organization', 'company', 'team', 'group', 'network',
        # Data & Information
        'data', 'information', 'knowledge', 'document', 'file',
        'database', 'model', 'representation', 'symbol',
        # Events & Actions
        'event', 'action', 'activity', 'task', 'operation',
        'incident', 'accident', 'problem', 'issue', 'challenge',
        # Quantities
        'number', 'value', 'amount', 'quantity', 'measure',
        'unit', 'percentage', 'ratio', 'rate',
        # Time & Space
        'time', 'moment', 'period', 'duration', 'frequency',
        'space', 'location', 'position', 'direction', 'distance',
        # Relations
        'relation', 'connection', 'link', 'association', 'dependency',
        # Attributes
        'property', 'attribute', 'characteristic', 'feature', 'quality',
        # States
        'state', 'condition', 'status', 'phase', 'stage',
        # Goals & Outcomes
        'goal', 'objective', 'target', 'purpose', 'intention',
        'result', 'outcome', 'effect', 'consequence', 'impact'
    }
    
    ACTIONS = {
        # Basic actions
        'create', 'destroy', 'build', 'make', 'produce', 'generate',
        'delete', 'remove', 'eliminate', 'erase', 'cancel',
        'modify', 'change', 'alter', 'adjust', 'update', 'transform',
        'move', 'transfer', 'transport', 'send', 'receive', 'get',
        # Cognitive actions
        'think', 'analyze', 'evaluate', 'assess', 'judge', 'decide',
        'learn', 'understand', 'comprehend', 'know', 'remember', 'forget',
        'plan', 'design', 'strategy', 'organize', 'arrange',
        # Communication
        'say', 'tell', 'ask', 'answer', 'explain', 'describe',
        'write', 'read', 'speak', 'listen', 'communicate',
        # Interaction
        'interact', 'collaborate', 'cooperate', 'compete', 'conflict',
        'help', 'assist', 'support', 'oppose', 'resist',
        # Control
        'control', 'manage', 'lead', 'follow', 'direct', 'guide',
        'start', 'stop', 'pause', 'resume', 'continue',
        # Measurement
        'measure', 'calculate', 'compute', 'estimate', 'predict',
        'compare', 'contrast', 'differentiate', 'classify', 'categorize'
    }
    
    RELATIONS = {
        # Logical relations
        'equals', 'differs', 'similar', 'opposite',
        # Spatial relations
        'above', 'below', 'inside', 'outside', 'between', 'among',
        'near', 'far', 'left', 'right', 'front', 'back',
        # Temporal relations
        'before', 'after', 'during', 'while', 'until', 'since',
        # Causal relations
        'causes', 'results_in', 'leads_to', 'prevents', 'enables',
        # Part-whole relations
        'contains', 'includes', 'part_of', 'member_of', 'component_of',
        # Ownership & Association
        'owns', 'belongs_to', 'associated_with', 'related_to',
        # Comparative relations
        'greater_than', 'less_than', 'equal_to', 'better_than', 'worse_than'
    }
    
    ATTRIBUTES = {
        # Physical attributes
        'size', 'weight', 'color', 'shape', 'texture', 'temperature',
        'speed', 'acceleration', 'force', 'energy', 'power',
        # Quantitative attributes
        'count', 'frequency', 'probability', 'confidence', 'accuracy',
        'efficiency', 'performance', 'capacity', 'limit', 'threshold',
        # Qualitative attributes
        'quality', 'importance', 'priority', 'urgency', 'difficulty',
        'complexity', 'simplicity', 'clarity', 'ambiguity',
        # State attributes
        'active', 'inactive', 'enabled', 'disabled', 'available',
        'busy', 'free', 'open', 'closed', 'locked', 'unlocked',
        # Evaluative attributes
        'good', 'bad', 'positive', 'negative', 'neutral',
        'successful', 'failed', 'correct', 'incorrect', 'optimal'
    }
    
    TEMPORAL = {
        'now', 'today', 'tomorrow', 'yesterday',
        'morning', 'afternoon', 'evening', 'night',
        'second', 'minute', 'hour', 'day', 'week', 'month', 'year',
        'past', 'present', 'future',
        'always', 'never', 'sometimes', 'often', 'rarely',
        'soon', 'later', 'earlier', 'immediately', 'eventually'
    }
    
    SPATIAL = {
        'here', 'there', 'everywhere', 'nowhere',
        'up', 'down', 'left', 'right', 'forward', 'backward',
        'north', 'south', 'east', 'west',
        'inside', 'outside', 'top', 'bottom', 'center',
        'local', 'remote', 'global', 'regional'
    }
    
    CAUSAL = {
        'because', 'therefore', 'thus', 'hence', 'consequently',
        'due_to', 'as_result', 'for_reason', 'in_order_to',
        'if_then', 'when_then', 'unless', 'otherwise'
    }
    
    MODALITY = {
        # Possibility
        'possible', 'impossible', 'probable', 'unlikely',
        # Necessity
        'necessary', 'required', 'mandatory', 'optional',
        # Ability
        'can', 'cannot', 'able', 'unable', 'capable',
        # Permission
        'allowed', 'forbidden', 'permitted', 'prohibited',
        # Belief
        'believe', 'know', 'uncertain', 'doubt', 'sure'
    }
    
    QUANTIFIER = {
        'all', 'every', 'each', 'some', 'any', 'none', 'no',
        'most', 'few', 'many', 'several', 'one', 'two', 'three',
        'first', 'last', 'next', 'previous', 'another', 'other'
    }
    
    NEGATION = {'not', 'no', 'never', 'none', 'neither', 'nobody', 'nothing'}
    
    CONDITIONAL = {'if', 'when', 'unless', 'provided', 'assuming', 'given'}
    
    QUERY = {'what', 'who', 'where', 'when', 'why', 'how', 'which', 'whose'}
    
    @classmethod
    def get_all_types(cls) -> Dict[str, set]:
        return {
            'ENTITY': cls.ENTITIES,
            'ACTION': cls.ACTIONS,
            'RELATION': cls.RELATIONS,
            'ATTRIBUTE': cls.ATTRIBUTES,
            'TEMPORAL': cls.TEMPORAL,
            'SPATIAL': cls.SPATIAL,
            'CAUSAL': cls.CAUSAL,
            'MODALITY': cls.MODALITY,
            'QUANTIFIER': cls.QUANTIFIER,
            'NEGATION': cls.NEGATION,
            'CONDITIONAL': cls.CONDITIONAL,
            'QUERY': cls.QUERY
        }


class SymbolicParser:
    """Main parser for converting natural language to symbolic expressions"""
    
    def __init__(self):
        self.ontology = UniversalOntology()
        self.type_markers = {
            '[': 'ENTITY',
            '<': 'ACTION',
            '{': 'RELATION',
            '@': 'ATTRIBUTE',
            '#': 'TEMPORAL',
            '$': 'SPATIAL',
            '!': 'CAUSAL',
            '?': 'MODALITY',
            '*': 'QUANTIFIER',
            '~': 'NEGATION',
            'IF_': 'CONDITIONAL',
            'QUERY_': 'QUERY'
        }
        
    def tokenize(self, text: str) -> List[str]:
        """Simple tokenization"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        # Split on spaces and punctuation (keeping punctuation)
        tokens = re.findall(r'\b\w+\b|[^\w\s]', text, re.UNICODE)
        return tokens
    
    def detect_type(self, word: str, context: List[str] = None) -> Tuple[str, float]:
        """Detect the symbolic type of a word"""
        word_lower = word.lower()
        
        # Check each ontology category
        ontology_types = self.ontology.get_all_types()
        
        for type_name, vocabulary in ontology_types.items():
            if word_lower in vocabulary:
                # Map to standard type names
                type_map = {
                    'ENTITY': 'ENTITY',
                    'ACTION': 'ACTION', 
                    'RELATION': 'RELATION',
                    'ATTRIBUTE': 'ATTRIBUTE',
                    'TEMPORAL': 'TEMPORAL',
                    'SPATIAL': 'SPATIAL',
                    'CAUSAL': 'CAUSAL',
                    'MODALITY': 'MODALITY',
                    'QUANTIFIER': 'QUANTIFIER',
                    'NEGATION': 'NEGATION',
                    'CONDITIONAL': 'CONDITIONAL',
                    'QUERY': 'QUERY'
                }
                return type_map.get(type_name, 'UNKNOWN'), 0.95
        
        # Default to entity for nouns (heuristic)
        if word_lower.isalpha() and len(word_lower) > 2:
            return 'ENTITY', 0.6
        
        return 'UNKNOWN', 0.3
    
    def parse(self, text: str) -> SymbolicExpression:
        """Parse natural language text into symbolic expression"""
        start_time = datetime.now()
        
        tokens = self.tokenize(text)
        symbols = []
        structure = {
            'subjects': [],
            'predicates': [],
            'objects': [],
            'modifiers': [],
            'relations': [],
            'temporal': [],
            'spatial': [],
            'causal': []
        }
        ontology_map = {}
        
        prev_symbol = None
        for i, token in enumerate(tokens):
            # Skip punctuation unless it's meaningful
            if token in '.,!?;:':
                continue
            
            symbol_type, confidence = self.detect_type(token, tokens[max(0,i-2):i+2])
            
            symbol = Symbol(
                type=symbol_type,
                value=token.lower(),
                original=token,
                confidence=confidence,
                metadata={'position': i}
            )
            
            symbols.append(symbol)
            ontology_map[token] = symbol_type
            
            # Build structure
            if symbol_type == 'ENTITY':
                if prev_symbol and prev_symbol.type == 'ACTION':
                    structure['objects'].append(token.lower())
                else:
                    structure['subjects'].append(token.lower())
            elif symbol_type == 'ACTION':
                structure['predicates'].append(token.lower())
            elif symbol_type == 'RELATION':
                structure['relations'].append(token.lower())
            elif symbol_type == 'ATTRIBUTE':
                structure['modifiers'].append(token.lower())
            elif symbol_type == 'TEMPORAL':
                structure['temporal'].append(token.lower())
            elif symbol_type == 'SPATIAL':
                structure['spatial'].append(token.lower())
            elif symbol_type == 'CAUSAL':
                structure['causal'].append(token.lower())
            
            prev_symbol = symbol
        
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds() * 1000
        
        expression = SymbolicExpression(
            id=f"sym_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
            input_text=text,
            symbols=symbols,
            structure=structure,
            ontology_map=ontology_map,
            timestamp=datetime.now().isoformat(),
            processing_time_ms=round(processing_time, 2)
        )
        
        return expression
    
    def parse_to_dict(self, text: str) -> Dict:
        """Parse and return as dictionary"""
        return self.parse(text).to_dict()
    
    def parse_to_string(self, text: str) -> str:
        """Parse and return as symbolic string"""
        return self.parse(text).to_string()


# Convenience function
def parse(text: str) -> SymbolicExpression:
    """Parse text into symbolic expression"""
    parser = SymbolicParser()
    return parser.parse(text)


if __name__ == "__main__":
    # Test examples
    test_cases = [
        "The robot moves quickly to the left",
        "If temperature increases then pressure will rise",
        "All students must complete the assignment before tomorrow",
        "The system cannot process requests when server is down",
        "Why did the machine stop working?",
        "Create a new user with admin privileges",
        "The algorithm optimizes performance by reducing memory usage"
    ]
    
    parser = SymbolicParser()
    
    print("=" * 80)
    print("UNIVERSAL SYMBOLIC LANGUAGE PARSER - PHASE 1")
    print("=" * 80)
    
    for test in test_cases:
        print(f"\nInput: {test}")
        result = parser.parse(test)
        print(f"Symbolic: {result.to_string()}")
        print(f"Structure: {json.dumps(result.structure, indent=2)}")
        print(f"Processing time: {result.processing_time_ms}ms")
        print("-" * 80)
