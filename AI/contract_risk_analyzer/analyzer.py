import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try loading spaCy model, download if not present
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    logger.info("Downloading spaCy en_core_web_sm model...")
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

class ContractAnalyzer:
    def __init__(self):
        logger.info("Initializing ContractAnalyzer and training ML model...")
        # 1. Simulate a trained ML model for risk classification based on Scikit-Learn
        self.vectorizer = TfidfVectorizer()
        
        # Simulated CUAD-like training data patterns
        training_texts = [
            "This agreement is strictly confidential and all secrets are maintained.",
            "The vendor shall indemnify the client against all claims.",
            "Either party may terminate this agreement with 30 days notice.",
            "The governing law will be the state of New York.",
            "The penalty for breach of contract is $1,000,000.",
            "The liability is unlimited for both parties.",
            "Force majeure events are excluded from liability.",
            "Any disputes will be resolved via binding arbitration.",
            "Failure to deliver by the due date results in immediate termination."
        ]
        
        # Risk Levels: 0: Low Risk, 1: Medium Risk, 2: High Risk
        labels = [0, 2, 0, 0, 2, 2, 1, 1, 2]
        
        X = self.vectorizer.fit_transform(training_texts)
        self.classifier = LogisticRegression()
        self.classifier.fit(X, labels)

    def extract_clauses(self, text):
        """Extract individual clauses (sentences) from the contract using spaCy."""
        doc = nlp(text)
        return [sent.text.strip() for sent in doc.sents if len(sent.text.strip()) > 5]

    def classify_risk(self, clause):
        """Classify a clause as Low, Medium, or High risk."""
        lower_clause = clause.lower()

        # Extra improvement
        if "shall pay" in lower_clause:
            return "Medium"

        high_risk_keywords = ["penalty", "termination", "liability", "breach", "indemnify"]
        medium_risk_keywords = ["delay", "payment", "pay", "obligation"]

        # Check HIGH first
        for word in high_risk_keywords:
            if word in lower_clause:
                return "High"

        # Then MEDIUM
        for word in medium_risk_keywords:
            if word in lower_clause:
                return "Medium"

        return "Low"

    def build_dependency_tree(self, doc):
        """Build dependency relationships for semantic understanding."""
        tree = []
        for token in doc:
            if not token.text.strip(): # Skip empty spaces and newlines
                continue
            tree.append({
                "word": token.text,
                "dep": token.dep_,
                "head": token.head.text
            })
        return tree

    def extract_entities(self, text):
        """Extract Named Entities (NER) like organizations, money, dates."""
        doc = nlp(text)
        return [{"text": ent.text, "label": ent.label_} for ent in doc.ents]

    def analyze(self, text):
        """Perform full contract analysis."""
        doc = nlp(text)
        clauses = self.extract_clauses(text)
        
        results = []
        high_risk = 0
        medium_risk = 0
        low_risk = 0

        for clause in clauses:
            if not clause: continue
            
            risk_level = self.classify_risk(clause)
            if risk_level == "High": high_risk += 1
            elif risk_level == "Medium": medium_risk += 1
            else: low_risk += 1

            # Extract NER per clause
            entities = self.extract_entities(clause)

            results.append({
                "clause": clause,
                "risk_level": risk_level,
                "entities": [f"{e['text']} ({e['label']})" for e in entities]
            })

        summary = f"Analyzed {len(clauses)} clauses. Found {high_risk} High risk, {medium_risk} Medium risk, and {low_risk} Low risk clauses."

        # Return partial dependency tree for UI so it doesn't get flooded
        dep_tree_sample = self.build_dependency_tree(doc)[:15] 

        return {
            "summary": summary,
            "clauses": results,
            "dependency_tree": dep_tree_sample
        }
