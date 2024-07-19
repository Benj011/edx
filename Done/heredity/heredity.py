import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]

def passDownProb(parent, one_gene, two_genes):
    if parent in one_gene:
        return 0.5
    elif parent in two_genes:
        return 1 - PROBS['mutation']
    else:
        return PROBS['mutation']


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """

    probability = 1.0

    # for person in people.keys():
    #     print(people[person]['mother'])


    parents = []
    children = []


    # add parents and children to their lists for easier access
    for person in people:
        if people[person]['mother'] == None:
            parents.append(person)
        else:
            children.append(person)


    # calculate the probability of the parents having the gene
    for person in parents:
        geneCount = 1 if person in one_gene else 2 if person in two_genes else 0
        probability *= PROBS['gene'][geneCount]

        # trait probability now
        probability *= PROBS['trait'][geneCount][person in have_trait]
        
    
    # calculate the probability of the children having the gene now

    for person in children:
        father = people[person]['father']
        fatherGeneCount = 1 if father in one_gene else 2 if father in two_genes else 0

        mother = people[person]['mother']
        motherGeneCount = 1 if mother in one_gene else 2 if mother in two_genes else 0

        # now child gene probability

        motherProb = passDownProb(mother, one_gene, two_genes)
        fatherProb = passDownProb(father, one_gene, two_genes)

        if person in one_gene:
            probability *= motherProb * (1 - fatherProb) + (1 - motherProb) * fatherProb
        elif person in two_genes:
            probability *= motherProb * fatherProb
        else:
            probability *= (1 - motherProb) * (1 - fatherProb)

        
            

        # now child trait probability
        
        if person in have_trait:
            geneCount = 1 if person in one_gene else 2 if person in two_genes else 0
            probability *= PROBS['trait'][geneCount][True]
        else:
            geneCount = 1 if person in one_gene else 2 if person in two_genes else 0
            probability *= PROBS['trait'][geneCount][False]

    return probability

    raise NotImplementedError


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """


    for person in probabilities:
        if person in one_gene:
            probabilities[person]["gene"][1] += p
        elif person in two_genes:
            probabilities[person]["gene"][2] += p
        else:
            probabilities[person]["gene"][0] += p

        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p

    return

    raise NotImplementedError


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """

    for person in probabilities:
        gene1 = probabilities[person]["gene"][1]
        gene2 = probabilities[person]["gene"][2]
        gene0 = probabilities[person]["gene"][0]

        if gene1 + gene2 + gene0 != 1:
            ratio = 1 / (gene1 + gene2 + gene0)
            probabilities[person]["gene"][1] *= ratio
            probabilities[person]["gene"][2] *= ratio
            probabilities[person]["gene"][0] *= ratio

        traitTrue = probabilities[person]["trait"][True]
        traitFalse = probabilities[person]["trait"][False]

        if traitTrue + traitFalse != 1:
            ratio = 1 / (traitTrue + traitFalse)
            probabilities[person]["trait"][True] *= ratio
            probabilities[person]["trait"][False] *= ratio

    return

    raise NotImplementedError


if __name__ == "__main__":
    main()

