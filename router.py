

from semantic_router import Route, SemanticRouter
from semantic_router.index import LocalIndex

from semantic_router.encoders import HuggingFaceEncoder

# Create the encoder
encoder = encoder = HuggingFaceEncoder(name="sentence-transformers/all-MiniLM-L6-v2")
 # Your routes defined





# Define routes
faq = Route(
    name="faq",
    utterances=[
        
        "What is the return policy of the products?",
        "Do I get discount with the credit card?",
        "How can I track my order?",
        "What payment methods are accepted?",
        "How long does it take to process a refund?",
        "What is your policy on defective products?",
        "What happens if the item I receive is damaged?",
        "Can I return a defective item?",
        "How do I claim a warranty for defective products?",
        "return policy",
        "refund policy",
        "how to get a refund",
        "can I return a product?",
    ]
)

sql = Route(
    name="sql",
    utterances=[
        "I want to buy nike shoes that have 50% discount.",
        "Are there any shoes under Rs. 3000?",
        "Do you have formal shoes in size 9?",
        "Are there any Puma shoes on sale?",
        "What is the price of puma running shoes?",
    ]
)

smalltalk = Route(
    name="smalltalk",
    utterances=[
        "hello",
        "hi",
        "hey",
        "how are you?",
        "what is your name?",
        "are you a robot?",
        "what are you?",
        "what do you do?",
    ]
)

# Group all routes
routes = [faq, sql, smalltalk]
index = LocalIndex()

# Create the SemanticRouter with auto index setup
router = SemanticRouter(
    encoder=encoder,
    routes=routes,
    auto_sync="local"  # Automatically builds and updates LocalIndex
)

# Test it
if __name__ == "__main__":
    print(router("Is their any return policy of the products?").name)   # → faq
    print(router("Pink Puma shoes in price range 5000 to 1000").name)  # → sql
    print(router("How are you?").name)                                 # → smalltalk
