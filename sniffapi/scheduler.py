import random
from faker import Faker
from sniffapi.models import ScentPost, Category, Tag
from django.contrib.auth.models import User

fake = Faker()

def generate_scent_title():
    """
    Generates a random scent title using descriptors commonly associated with scents.
    """
    descriptors = ['best', 'worst', 'regular']
    title = f"{random.choice(descriptors).capitalize()} Smell"
    return title

def generate_scent_description():
    """
    Generates a random scent description using Faker.
    """
    descriptors = ['gross', 'nasty', 'amazing']
    notes = ['top notes', 'middle notes', 'base notes']
    description = f"A {random.choice(descriptors)} scent with {random.choice(notes)} of {fake.word()}, {fake.word()}, and {fake.word()}."
    return description

def create_scent_post():
    # Get a random user instance
    users = User.objects.all()
    user = random.choice(users) if users else None

    # Get a random category instance
    categories = Category.objects.all()
    category = random.choice(categories) if categories else None

    
    # Generate random title with a specific keyword and random description describing a scent
    title = generate_scent_title()
    description = generate_scent_description()  # Generating a random sentence for description


    # Create a new ScentPost instance
    scent_post = ScentPost.objects.create(
        user=user,
        title=title,
        description=description,
        category=category
    )

    # Add random tags
    tags = Tag.objects.all()
    random_tags = random.sample(list(tags), random.randint(1, 3))  # Select 1 to 5 random tags
    for tag in random_tags:
        scent_post.tags.add(tag)

          