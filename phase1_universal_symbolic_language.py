"""
PHASE 1: Universal Symbolic Language System

This module implements a comprehensive symbolic language that can represent
ANY concept, entity, action, relation, attribute, temporal/spatial/causal
elements - not just emotions.

Symbolic Grammar:
- ENTITY: Objects, concepts, agents (e.g., [USER], [PRODUCT], [PROBLEM])
- ACTION: Verbs, operations, processes (e.g., <BUY>, <ANALYZE>, <CREATE>)
- RELATION: Connections between entities (e.g., {OWNS}, {CAUSES}, {PART_OF})
- ATTRIBUTE: Properties and qualities (e.g., @COLOR=red, @SIZE=large)
- TEMPORAL: Time-related markers (e.g., #PAST, #FUTURE, #DURING)
- SPATIAL: Location and position (e.g., $HERE, $THERE, $INSIDE)
- CAUSAL: Cause-effect chains (e.g., !LEADS_TO, !PREVENTS, !REQUIRES)
- MODALITY: Certainty, possibility, necessity (e.g., ?MAYBE, !MUST, ~IMPOSSIBLE)
- QUANTIFIER: Amounts and scopes (e.g., *ALL, *SOME, *NONE, *MANY)

Example: 
  "The user bought a red product yesterday"
  → [USER] <BUY> [PRODUCT] @COLOR=red #PAST
"""

from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Set, Tuple, Union
import json
import hashlib
from datetime import datetime
import re


class SymbolType(Enum):
    """Types of symbolic elements"""
    ENTITY = auto()      # Objects, concepts, agents
    ACTION = auto()      # Verbs, operations, processes
    RELATION = auto()    # Connections between entities
    ATTRIBUTE = auto()   # Properties and qualities
    TEMPORAL = auto()    # Time-related markers
    SPATIAL = auto()     # Location and position
    CAUSAL = auto()      # Cause-effect relationships
    MODALITY = auto()    # Certainty, possibility, necessity
    QUANTIFIER = auto()  # Amounts and scopes
    NEGATION = auto()    # Negation operators
    CONDITIONAL = auto() # If-then structures
    QUERY = auto()       # Questions and queries


class OntologyCategory(Enum):
    """Universal ontology categories"""
    PHYSICAL_OBJECT = auto()
    ABSTRACT_CONCEPT = auto()
    AGENT = auto()
    EVENT = auto()
    STATE = auto()
    PROCESS = auto()
    PROPERTY = auto()
    RELATION = auto()
    QUANTITY = auto()
    TIME = auto()
    SPACE = auto()
    EMOTION = auto()
    INTENT = auto()
    BELIEF = auto()
    KNOWLEDGE = auto()


@dataclass
class Symbol:
    """Base class for all symbolic elements"""
    symbol_type: SymbolType
    value: str
    category: Optional[OntologyCategory] = None
    confidence: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    parent: Optional['Symbol'] = None
    children: List['Symbol'] = field(default_factory=list)
    relations: List['SymbolRelation'] = field(default_factory=list)
    
    def __hash__(self):
        return hash((self.symbol_type, self.value))
    
    def __eq__(self, other):
        if not isinstance(other, Symbol):
            return False
        return self.symbol_type == other.symbol_type and self.value == other.value
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert symbol to dictionary representation"""
        return {
            'type': self.symbol_type.name,
            'value': self.value,
            'category': self.category.name if self.category else None,
            'confidence': self.confidence,
            'metadata': self.metadata,
            'children': [child.to_dict() for child in self.children],
            'relations': [rel.to_dict() for rel in self.relations]
        }
    
    def to_string(self) -> str:
        """Convert symbol to string representation"""
        prefix_map = {
            SymbolType.ENTITY: '[',
            SymbolType.ACTION: '<',
            SymbolType.RELATION: '{',
            SymbolType.ATTRIBUTE: '@',
            SymbolType.TEMPORAL: '#',
            SymbolType.SPATIAL: '$',
            SymbolType.CAUSAL: '!',
            SymbolType.MODALITY: '?',
            SymbolType.QUANTIFIER: '*',
            SymbolType.NEGATION: '~',
            SymbolType.CONDITIONAL: 'IF_',
            SymbolType.QUERY: '?'
        }
        
        suffix_map = {
            SymbolType.ENTITY: ']',
            SymbolType.ACTION: '>',
            SymbolType.RELATION: '}',
        }
        
        prefix = prefix_map.get(self.symbol_type, '')
        suffix = suffix_map.get(self.symbol_type, '')
        
        if self.symbol_type == SymbolType.ATTRIBUTE:
            if '=' in self.value:
                key, val = self.value.split('=', 1)
                return f"@{key}={val}"
        
        return f"{prefix}{self.value}{suffix}"
    
    def add_child(self, child: 'Symbol'):
        """Add a child symbol"""
        child.parent = self
        self.children.append(child)
    
    def add_relation(self, relation: 'SymbolRelation'):
        """Add a relation to this symbol"""
        self.relations.append(relation)
    
    def get_id(self) -> str:
        """Generate unique ID for this symbol"""
        content = f"{self.symbol_type.name}:{self.value}:{self.category.name if self.category else ''}"
        return hashlib.md5(content.encode()).hexdigest()[:12]


@dataclass
class SymbolRelation:
    """Represents a relation between two symbols"""
    source: Symbol
    target: Symbol
    relation_type: Symbol
    direction: str = 'forward'  # forward, backward, bidirectional
    strength: float = 1.0
    temporal_context: Optional[Symbol] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'source': self.source.value,
            'target': self.target.value,
            'relation_type': self.relation_type.value,
            'direction': self.direction,
            'strength': self.strength,
            'temporal_context': self.temporal_context.value if self.temporal_context else None
        }


@dataclass
class SymbolicExpression:
    """A complete symbolic expression representing a concept, statement, or query"""
    id: str
    symbols: List[Symbol]
    root_symbol: Optional[Symbol] = None
    creation_time: datetime = field(default_factory=datetime.now)
    source_text: Optional[str] = None
    confidence: float = 1.0
    context: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'symbols': [sym.to_dict() for sym in self.symbols],
            'root_symbol': self.root_symbol.to_dict() if self.root_symbol else None,
            'creation_time': self.creation_time.isoformat(),
            'source_text': self.source_text,
            'confidence': self.confidence,
            'context': self.context
        }
    
    def to_string(self) -> str:
        """Convert entire expression to string representation"""
        return ' '.join(sym.to_string() for sym in self.symbols)
    
    def get_entities(self) -> List[Symbol]:
        """Get all entity symbols"""
        return [s for s in self.symbols if s.symbol_type == SymbolType.ENTITY]
    
    def get_actions(self) -> List[Symbol]:
        """Get all action symbols"""
        return [s for s in self.symbols if s.symbol_type == SymbolType.ACTION]
    
    def get_relations(self) -> List[Symbol]:
        """Get all relation symbols"""
        return [s for s in self.symbols if s.symbol_type == SymbolType.RELATION]


class UniversalSymbolicLexer:
    """Tokenizes natural language into preliminary symbolic tokens"""
    
    def __init__(self):
        # Comprehensive pattern library for universal domain coverage
        self.patterns = {
            # Entities
            'entity_bracket': r'\[([A-Z_][A-Z0-9_]*)\]',
            'entity_capitalized': r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b',
            'entity_pronoun': r'\b(I|you|he|she|it|we|they|me|him|her|us|them)\b',
            
            # Actions
            'action_bracket': r'<([A-Z_][A-Z0-9_]*)>',
            'action_verb': r'\b(achieve|analyze|build|buy|calculate|change|check|choose|create|decide|define|delete|design|detect|determine|develop|discover|enable|evaluate|execute|explain|explore|find|fix|generate|get|give|have|help|identify|implement|improve|increase|learn|make|measure|modify|move|need|obtain|optimize|perform|plan|predict|prevent|process|produce|provide|query|reduce|resolve|run|save|search|select|send|set|solve|start|stop|study|take|test|transform|understand|update|use|validate|verify|want|work|write)\b',
            
            # Relations
            'relation_bracket': r'\{([A-Z_][A-Z0-9_]*)\}',
            'relation_preposition': r'\b(in|on|at|by|for|with|from|to|of|about|into|through|during|before|after|above|below|between|among|without|despite|like|unlike|as)\b',
            'relation_verb_form': r'\b(has|have|had|is|are|was|were|be|been|being|contains|includes|comprises|consists|belongs|owns|possesses|causes|creates|produces|prevents|stops|blocks|requires|needs|demands|enables|allows|permits)\b',
            
            # Attributes
            'attribute_bracket': r'@([A-Za-z_][A-Za-z0-9_]*)=([^\s,]+)',
            'attribute_adjective': r'\b([a-z]+(?:-[a-z]+)*)(?=\s+(?:noun|entity|object|thing|person))\b',
            
            # Temporal
            'temporal_bracket': r'#([A-Z_][A-Z0-9_]*)',
            'temporal_word': r'\b(yesterday|today|tomorrow|now|then|soon|later|earlier|before|after|during|while|when|always|never|sometimes|often|rarely|frequently|occasionally|morning|afternoon|evening|night|week|month|year|century|moment|instant|period|era|age)\b',
            
            # Spatial
            'spatial_bracket': r'\$([A-Z_][A-Z0-9_]*)',
            'spatial_word': r'\b(here|there|everywhere|nowhere|somewhere|inside|outside|above|below|top|bottom|left|right|front|back|north|south|east|west|up|down|near|far|close|distant|adjacent|opposite|within|beyond|throughout|across|along|around|behind|beside|between|among)\b',
            
            # Causal
            'causal_bracket': r'!([A-Z_][A-Z0-9_]*)',
            'causal_word': r'\b(because|since|therefore|thus|hence|consequently|accordingly|so|then|if|unless|provided|given|assuming|leads to|results in|causes|creates|produces|triggers|generates|brings about|gives rise to|stems from|arises from|originates from|due to|owing to|thanks to)\b',
            
            # Modality
            'modality_bracket': r'\?([A-Z_][A-Z0-9_]*)',
            'modality_word': r'\b(maybe|perhaps|possibly|probably|certainly|definitely|absolutely|clearly|obviously|surely|indeed|must|should|could|would|might|may|can|will|shall|ought to|have to|need to|required to|necessary|essential|important|possible|impossible|probable|uncertain|unknown)\b',
            
            # Quantifiers
            'quantifier_bracket': r'\*([A-Z_][A-Z0-9_]*)',
            'quantifier_word': r'\b(all|every|each|some|any|no|none|nothing|something|anything|everything|much|many|few|little|several|most|least|more|less|enough|sufficient|adequate|plenty|abundance|majority|minority|half|quarter|third|double|triple|single|pair|couple|group|set|collection|series|sequence)\b',
            
            # Negation
            'negation_bracket': r'~([A-Z_][A-Z0-9_]*)',
            'negation_word': r'\b(not|no|never|neither|nor|none|nothing|nowhere|nobody|no one|cannot|can\'t|won\'t|wouldn\'t|shouldn\'t|mustn\'t|don\'t|doesn\'t|didn\'t|isn\'t|aren\'t|wasn\'t|weren\'t|haven\'t|hasn\'t|hadn\'t|without|lacking|absence|lack|deny|refuse|reject|oppose|contrary|opposite|inverse|reverse|negative)\b',
            
            # Conditional
            'conditional_word': r'\b(if|then|else|otherwise|unless|provided that|in case|whenever|every time|as long as|on condition that|supposing|assuming|given that|considering|in the event that|should|would that)\b',
            
            # Query
            'query_word': r'\b(what|who|whom|whose|which|where|when|why|how|whether|if|what if|how many|how much|how often|how long|how far|how deep|how high|how wide|what kind|what type|which one|whose turn|where from|where to|when ever|why not|how come)\b',
        }
        
        self.stopwords = {
            'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'dare', 'ought',
            'used', 'it', 'its', 'this', 'that', 'these', 'those', 'i', 'you', 'he',
            'she', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his',
            'our', 'their', 'mine', 'yours', 'hers', 'ours', 'theirs', 'what', 'which',
            'who', 'whom', 'whose', 'where', 'when', 'why', 'how', 'all', 'each', 'every',
            'both', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
            'only', 'own', 'same', 'so', 'than', 'too', 'very', 'just', 'also', 'now',
            'here', 'there', 'then', 'once', 'if', 'because', 'until', 'while', 'about',
            'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above',
            'below', 'up', 'down', 'out', 'off', 'over', 'under', 'again', 'further',
            'am', 'being', 'do', 'doing', 'have', 'having', 'has', 'had', 'having'
        }
    
    def tokenize(self, text: str) -> List[Dict[str, Any]]:
        """Convert text to preliminary tokens"""
        tokens = []
        words = re.findall(r'\b\w+\b|[<>\[\]{}@$!?*~]', text)
        
        for i, word in enumerate(words):
            if word.lower() in self.stopwords and len(word) < 4:
                continue
            
            token = {'text': word, 'position': i, 'types': []}
            
            # Check against all patterns
            for token_type, pattern in self.patterns.items():
                if re.match(pattern, word, re.IGNORECASE):
                    token['types'].append(token_type)
            
            tokens.append(token)
        
        return tokens


class UniversalSymbolicParser:
    """Parses tokens into structured symbolic expressions"""
    
    def __init__(self):
        self.lexer = UniversalSymbolicLexer()
        
        # Universal ontology mapping
        self.entity_ontology = {
            'USER': OntologyCategory.AGENT,
            'PERSON': OntologyCategory.AGENT,
            'PEOPLE': OntologyCategory.AGENT,
            'CUSTOMER': OntologyCategory.AGENT,
            'CLIENT': OntologyCategory.AGENT,
            'AGENT': OntologyCategory.AGENT,
            'SYSTEM': OntologyCategory.AGENT,
            'AI': OntologyCategory.AGENT,
            'ROBOT': OntologyCategory.AGENT,
            'ORGANIZATION': OntologyCategory.AGENT,
            'COMPANY': OntologyCategory.AGENT,
            'TEAM': OntologyCategory.AGENT,
            
            'PRODUCT': OntologyCategory.PHYSICAL_OBJECT,
            'ITEM': OntologyCategory.PHYSICAL_OBJECT,
            'OBJECT': OntologyCategory.PHYSICAL_OBJECT,
            'DEVICE': OntologyCategory.PHYSICAL_OBJECT,
            'MACHINE': OntologyCategory.PHYSICAL_OBJECT,
            'TOOL': OntologyCategory.PHYSICAL_OBJECT,
            'EQUIPMENT': OntologyCategory.PHYSICAL_OBJECT,
            'MATERIAL': OntologyCategory.PHYSICAL_OBJECT,
            'SUBSTANCE': OntologyCategory.PHYSICAL_OBJECT,
            
            'PROBLEM': OntologyCategory.ABSTRACT_CONCEPT,
            'SOLUTION': OntologyCategory.ABSTRACT_CONCEPT,
            'IDEA': OntologyCategory.ABSTRACT_CONCEPT,
            'CONCEPT': OntologyCategory.ABSTRACT_CONCEPT,
            'THEORY': OntologyCategory.ABSTRACT_CONCEPT,
            'PRINCIPLE': OntologyCategory.ABSTRACT_CONCEPT,
            'RULE': OntologyCategory.ABSTRACT_CONCEPT,
            'LAW': OntologyCategory.ABSTRACT_CONCEPT,
            'MODEL': OntologyCategory.ABSTRACT_CONCEPT,
            'FRAMEWORK': OntologyCategory.ABSTRACT_CONCEPT,
            
            'EVENT': OntologyCategory.EVENT,
            'INCIDENT': OntologyCategory.EVENT,
            'OCCURRENCE': OntologyCategory.EVENT,
            'SITUATION': OntologyCategory.STATE,
            'CONDITION': OntologyCategory.STATE,
            'STATE': OntologyCategory.STATE,
            'STATUS': OntologyCategory.STATE,
            
            'PROCESS': OntologyCategory.PROCESS,
            'PROCEDURE': OntologyCategory.PROCESS,
            'METHOD': OntologyCategory.PROCESS,
            'TECHNIQUE': OntologyCategory.PROCESS,
            'APPROACH': OntologyCategory.PROCESS,
            'STRATEGY': OntologyCategory.PROCESS,
            'PLAN': OntologyCategory.PROCESS,
            
            'EMOTION': OntologyCategory.EMOTION,
            'FEELING': OntologyCategory.EMOTION,
            'MOOD': OntologyCategory.EMOTION,
            'SENTIMENT': OntologyCategory.EMOTION,
            
            'INTENT': OntologyCategory.INTENT,
            'GOAL': OntologyCategory.INTENT,
            'OBJECTIVE': OntologyCategory.INTENT,
            'PURPOSE': OntologyCategory.INTENT,
            'AIM': OntologyCategory.INTENT,
            
            'BELIEF': OntologyCategory.BELIEF,
            'OPINION': OntologyCategory.BELIEF,
            'VIEW': OntologyCategory.BELIEF,
            'PERSPECTIVE': OntologyCategory.BELIEF,
            
            'KNOWLEDGE': OntologyCategory.KNOWLEDGE,
            'INFORMATION': OntologyCategory.KNOWLEDGE,
            'DATA': OntologyCategory.KNOWLEDGE,
            'FACT': OntologyCategory.KNOWLEDGE,
            'EVIDENCE': OntologyCategory.KNOWLEDGE,
        }
        
        self.action_ontology = {
            'BUY': OntologyCategory.EVENT,
            'SELL': OntologyCategory.EVENT,
            'CREATE': OntologyCategory.PROCESS,
            'DESTROY': OntologyCategory.PROCESS,
            'BUILD': OntologyCategory.PROCESS,
            'MAKE': OntologyCategory.PROCESS,
            'DESIGN': OntologyCategory.PROCESS,
            'DEVELOP': OntologyCategory.PROCESS,
            'ANALYZE': OntologyCategory.PROCESS,
            'EVALUATE': OntologyCategory.PROCESS,
            'MEASURE': OntologyCategory.PROCESS,
            'CALCULATE': OntologyCategory.PROCESS,
            'COMPUTE': OntologyCategory.PROCESS,
            'THINK': OntologyCategory.PROCESS,
            'LEARN': OntologyCategory.PROCESS,
            'UNDERSTAND': OntologyCategory.PROCESS,
            'KNOW': OntologyCategory.STATE,
            'BELIEVE': OntologyCategory.STATE,
            'FEEL': OntologyCategory.STATE,
            'WANT': OntologyCategory.STATE,
            'NEED': OntologyCategory.STATE,
            'HAVE': OntologyCategory.STATE,
            'OWN': OntologyCategory.STATE,
            'POSSESS': OntologyCategory.STATE,
        }
    
    def parse(self, text: str) -> SymbolicExpression:
        """Parse natural language text into symbolic expression"""
        tokens = self.lexer.tokenize(text)
        symbols = []
        
        for token in tokens:
            symbol = self._token_to_symbol(token)
            if symbol:
                symbols.append(symbol)
        
        # Build relations between symbols
        self._build_relations(symbols)
        
        # Determine root symbol
        root_symbol = self._find_root_symbol(symbols)
        
        # Generate ID
        expr_id = hashlib.md5(f"{text}:{datetime.now().isoformat()}".encode()).hexdigest()[:12]
        
        return SymbolicExpression(
            id=expr_id,
            symbols=symbols,
            root_symbol=root_symbol,
            source_text=text
        )
    
    def _token_to_symbol(self, token: Dict[str, Any]) -> Optional[Symbol]:
        """Convert a token to a Symbol"""
        text = token['text']
        types = token['types']
        
        # Priority mapping - check most specific patterns first
        priority_order = [
            'entity_bracket', 'action_bracket', 'relation_bracket', 
            'attribute_bracket', 'temporal_bracket', 'spatial_bracket',
            'causal_bracket', 'modality_bracket', 'quantifier_bracket',
            'negation_bracket',
            'action_verb', 'temporal_word', 'spatial_word', 'causal_word',
            'modality_word', 'quantifier_word', 'negation_word',
            'conditional_word', 'query_word',
            'relation_preposition', 'relation_verb_form',
            'entity_capitalized', 'entity_pronoun'
        ]
        
        for token_type in priority_order:
            if token_type in types:
                return self._create_symbol_from_type(token_type, text)
        
        # Fallback: try to infer from word itself
        return self._infer_symbol_type(text)
    
    def _create_symbol_from_type(self, token_type: str, text: str) -> Optional[Symbol]:
        """Create symbol based on token type"""
        type_mapping = {
            'entity_bracket': (SymbolType.ENTITY, text[1:-1]),
            'entity_capitalized': (SymbolType.ENTITY, text.upper()),
            'entity_pronoun': (SymbolType.ENTITY, text.upper()),
            'action_bracket': (SymbolType.ACTION, text[1:-1]),
            'action_verb': (SymbolType.ACTION, text.upper()),
            'relation_bracket': (SymbolType.RELATION, text[1:-1]),
            'relation_preposition': (SymbolType.RELATION, text.upper()),
            'relation_verb_form': (SymbolType.RELATION, text.upper()),
            'attribute_bracket': (SymbolType.ATTRIBUTE, text[1:]),
            'temporal_bracket': (SymbolType.TEMPORAL, text[1:]),
            'temporal_word': (SymbolType.TEMPORAL, text.upper()),
            'spatial_bracket': (SymbolType.SPATIAL, text[1:]),
            'spatial_word': (SymbolType.SPATIAL, text.upper()),
            'causal_bracket': (SymbolType.CAUSAL, text[1:]),
            'causal_word': (SymbolType.CAUSAL, text.upper().replace(' ', '_')),
            'modality_bracket': (SymbolType.MODALITY, text[1:]),
            'modality_word': (SymbolType.MODALITY, text.upper()),
            'quantifier_bracket': (SymbolType.QUANTIFIER, text[1:]),
            'quantifier_word': (SymbolType.QUANTIFIER, text.upper()),
            'negation_bracket': (SymbolType.NEGATION, text[1:]),
            'negation_word': (SymbolType.NEGATION, text.upper()),
            'conditional_word': (SymbolType.CONDITIONAL, text.upper().replace(' ', '_')),
            'query_word': (SymbolType.QUERY, text.upper().replace(' ', '_')),
        }
        
        if token_type not in type_mapping:
            return None
        
        sym_type, value = type_mapping[token_type]
        
        # Handle attribute special case
        if sym_type == SymbolType.ATTRIBUTE and '=' not in value:
            return None
        
        # Determine ontology category
        category = None
        if sym_type == SymbolType.ENTITY:
            category = self.entity_ontology.get(value, OntologyCategory.ABSTRACT_CONCEPT)
        elif sym_type == SymbolType.ACTION:
            category = self.action_ontology.get(value, OntologyCategory.PROCESS)
        elif sym_type == SymbolType.TEMPORAL:
            category = OntologyCategory.TIME
        elif sym_type == SymbolType.SPATIAL:
            category = OntologyCategory.SPACE
        
        return Symbol(
            symbol_type=sym_type,
            value=value,
            category=category
        )
    
    def _infer_symbol_type(self, text: str) -> Optional[Symbol]:
        """Infer symbol type from text when no explicit markers"""
        text_lower = text.lower()
        
        # Check various categories
        if text_lower in self.lexer.patterns.get('temporal_word', ''):
            return Symbol(SymbolType.TEMPORAL, text.upper(), OntologyCategory.TIME)
        elif text_lower in self.lexer.patterns.get('spatial_word', ''):
            return Symbol(SymbolType.SPATIAL, text.upper(), OntologyCategory.SPACE)
        elif text_lower in self.lexer.patterns.get('causal_word', ''):
            return Symbol(SymbolType.CAUSAL, text.upper().replace(' ', '_'))
        elif text_lower in self.lexer.patterns.get('modality_word', ''):
            return Symbol(SymbolType.MODALITY, text.upper())
        elif text_lower in self.lexer.patterns.get('quantifier_word', ''):
            return Symbol(SymbolType.QUANTIFIER, text.upper())
        elif text_lower in self.lexer.patterns.get('negation_word', ''):
            return Symbol(SymbolType.NEGATION, text.upper())
        elif text_lower in self.lexer.patterns.get('query_word', ''):
            return Symbol(SymbolType.QUERY, text.upper().replace(' ', '_'))
        elif text_lower in self.lexer.patterns.get('action_verb', ''):
            return Symbol(SymbolType.ACTION, text.upper(), OntologyCategory.PROCESS)
        elif text[0].isupper() and len(text) > 1:
            return Symbol(SymbolType.ENTITY, text.upper(), OntologyCategory.ABSTRACT_CONCEPT)
        
        return None
    
    def _build_relations(self, symbols: List[Symbol]):
        """Build relations between symbols based on proximity and type"""
        for i, sym in enumerate(symbols):
            if sym.symbol_type == SymbolType.ENTITY:
                # Look for actions nearby
                for j in range(max(0, i-3), min(len(symbols), i+4)):
                    if j != i and symbols[j].symbol_type == SymbolType.ACTION:
                        relation = SymbolRelation(
                            source=sym,
                            target=symbols[j],
                            relation_type=Symbol(SymbolType.RELATION, 'PERFORMS')
                        )
                        sym.add_relation(relation)
    
    def _find_root_symbol(self, symbols: List[Symbol]) -> Optional[Symbol]:
        """Find the root symbol (usually main action or primary entity)"""
        # Priority: ACTION > ENTITY > RELATION
        for sym in symbols:
            if sym.symbol_type == SymbolType.ACTION:
                return sym
        
        for sym in symbols:
            if sym.symbol_type == SymbolType.ENTITY:
                return sym
        
        return symbols[0] if symbols else None


class UniversalSymbolicComposer:
    """Composes complex symbolic expressions from simpler ones"""
    
    def compose(self, expressions: List[SymbolicExpression], operation: str) -> SymbolicExpression:
        """Compose multiple expressions using specified operation"""
        if operation == 'CONJUNCTION':
            return self._conjunction(expressions)
        elif operation == 'DISJUNCTION':
            return self._disjunction(expressions)
        elif operation == 'IMPLICATION':
            return self._implication(expressions)
        elif operation == 'NEGATION':
            return self._negation(expressions[0])
        elif operation == 'QUANTIFICATION':
            return self._quantification(expressions)
        else:
            raise ValueError(f"Unknown composition operation: {operation}")
    
    def _conjunction(self, expressions: List[SymbolicExpression]) -> SymbolicExpression:
        """Combine expressions with AND logic"""
        all_symbols = []
        for expr in expressions:
            all_symbols.extend(expr.symbols)
        
        # Add conjunction marker
        and_symbol = Symbol(SymbolType.RELATION, 'AND')
        all_symbols.insert(len(all_symbols)//2, and_symbol)
        
        expr_id = hashlib.md5(f"CONJ:{datetime.now().isoformat()}".encode()).hexdigest()[:12]
        return SymbolicExpression(
            id=expr_id,
            symbols=all_symbols,
            root_symbol=expressions[0].root_symbol
        )
    
    def _disjunction(self, expressions: List[SymbolicExpression]) -> SymbolicExpression:
        """Combine expressions with OR logic"""
        all_symbols = []
        for i, expr in enumerate(expressions):
            if i > 0:
                all_symbols.append(Symbol(SymbolType.RELATION, 'OR'))
            all_symbols.extend(expr.symbols)
        
        expr_id = hashlib.md5(f"DISJ:{datetime.now().isoformat()}".encode()).hexdigest()[:12]
        return SymbolicExpression(
            id=expr_id,
            symbols=all_symbols,
            root_symbol=expressions[0].root_symbol
        )
    
    def _implication(self, expressions: List[SymbolicExpression]) -> SymbolicExpression:
        """Create IF-THEN implication"""
        if len(expressions) < 2:
            raise ValueError("Implication requires at least 2 expressions")
        
        antecedent = expressions[0]
        consequent = expressions[1]
        
        symbols = [Symbol(SymbolType.CONDITIONAL, 'IF')]
        symbols.extend(antecedent.symbols)
        symbols.append(Symbol(SymbolType.CONDITIONAL, 'THEN'))
        symbols.extend(consequent.symbols)
        
        expr_id = hashlib.md5(f"IMPL:{datetime.now().isoformat()}".encode()).hexdigest()[:12]
        return SymbolicExpression(
            id=expr_id,
            symbols=symbols,
            root_symbol=Symbol(SymbolType.CONDITIONAL, 'IMPLIES')
        )
    
    def _negation(self, expression: SymbolicExpression) -> SymbolicExpression:
        """Negate an expression"""
        symbols = [Symbol(SymbolType.NEGATION, 'NOT')]
        symbols.extend(expression.symbols)
        
        expr_id = hashlib.md5(f"NEG:{datetime.now().isoformat()}".encode()).hexdigest()[:12]
        return SymbolicExpression(
            id=expr_id,
            symbols=symbols,
            root_symbol=Symbol(SymbolType.NEGATION, 'NEGATION')
        )
    
    def _quantification(self, expressions: List[SymbolicExpression]) -> SymbolicExpression:
        """Apply quantifiers to expressions"""
        if len(expressions) < 2:
            raise ValueError("Quantification requires quantifier and expression")
        
        quantifier_expr = expressions[0]
        target_expr = expressions[1]
        
        symbols = quantifier_expr.symbols + target_expr.symbols
        
        expr_id = hashlib.md5(f"QUANT:{datetime.now().isoformat()}".encode()).hexdigest()[:12]
        return SymbolicExpression(
            id=expr_id,
            symbols=symbols,
            root_symbol=quantifier_expr.root_symbol
        )


class SymbolicLanguageEngine:
    """Main engine for universal symbolic language processing"""
    
    def __init__(self):
        self.parser = UniversalSymbolicParser()
        self.composer = UniversalSymbolicComposer()
        self.expression_cache: Dict[str, SymbolicExpression] = {}
    
    def parse_to_symbols(self, text: str) -> SymbolicExpression:
        """Parse natural language to symbolic expression"""
        if text in self.expression_cache:
            return self.expression_cache[text]
        
        expression = self.parser.parse(text)
        self.expression_cache[text] = expression
        return expression
    
    def compose_expressions(self, expressions: List[SymbolicExpression], operation: str) -> SymbolicExpression:
        """Compose multiple expressions"""
        return self.composer.compose(expressions, operation)
    
    def symbol_to_natural_language(self, expression: SymbolicExpression) -> str:
        """Convert symbolic expression back to natural language (simplified)"""
        parts = []
        for sym in expression.symbols:
            if sym.symbol_type == SymbolType.ENTITY:
                parts.append(sym.value.lower())
            elif sym.symbol_type == SymbolType.ACTION:
                parts.append(sym.value.lower())
            elif sym.symbol_type == SymbolType.RELATION:
                parts.append(sym.value.lower())
            elif sym.symbol_type == SymbolType.ATTRIBUTE:
                if '=' in sym.value:
                    key, val = sym.value.split('=', 1)
                    parts.append(f"{key} is {val}")
            # Add more conversions as needed
        
        return ' '.join(parts)
    
    def get_expression_statistics(self, expression: SymbolicExpression) -> Dict[str, Any]:
        """Get statistics about an expression"""
        stats = {
            'total_symbols': len(expression.symbols),
            'entities': len(expression.get_entities()),
            'actions': len(expression.get_actions()),
            'relations': len(expression.get_relations()),
            'symbol_types': {}
        }
        
        for sym in expression.symbols:
            type_name = sym.symbol_type.name
            stats['symbol_types'][type_name] = stats['symbol_types'].get(type_name, 0) + 1
        
        return stats
    
    def export_expression(self, expression: SymbolicExpression, format: str = 'json') -> str:
        """Export expression in specified format"""
        if format == 'json':
            return json.dumps(expression.to_dict(), indent=2)
        elif format == 'string':
            return expression.to_string()
        else:
            raise ValueError(f"Unsupported export format: {format}")


# Example usage and testing
if __name__ == "__main__":
    engine = SymbolicLanguageEngine()
    
    # Test cases covering various domains
    test_cases = [
        # Customer support (original domain)
        "The customer is angry about the delayed product",
        "I want to cancel my order immediately",
        
        # Scientific reasoning
        "The experiment proves the hypothesis",
        "Temperature increases cause pressure to rise",
        
        # Business decisions
        "The company should invest in new technology",
        "Market analysis indicates growth opportunities",
        
        # Everyday reasoning
        "If it rains, then the game will be cancelled",
        "All humans need water to survive",
        
        # Complex multi-entity scenarios
        "The doctor prescribed medicine to the patient because the disease was serious",
        "The robot assembled the product in the factory yesterday"
    ]
    
    print("=" * 80)
    print("PHASE 1: Universal Symbolic Language System - Test Results")
    print("=" * 80)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test}")
        print("-" * 60)
        
        expr = engine.parse_to_symbols(test)
        print(f"Symbolic: {expr.to_string()}")
        print(f"Statistics: {engine.get_expression_statistics(expr)}")
        print(f"JSON Preview: {engine.export_expression(expr, 'json')[:200]}...")
    
    print("\n" + "=" * 80)
    print("Phase 1 Complete: Universal Symbolic Language System Ready")
    print("=" * 80)
