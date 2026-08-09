class DialogueNode:

    def __init__(
        self,
        node_id,
        text,
        options=None
    ):
        self.node_id = node_id
        self.text = text
        self.options = options or {}


class DialogueTree:

    def __init__(
        self,
        start_node_id="start"
    ):
        self.nodes = {}

        self.start_node_id = (
            start_node_id
        )

        self.current_node_id = (
            start_node_id
        )

    # Add a new dialogue node.
    def add_node(self, node):

        self.nodes[
            node.node_id
        ] = node

    # Get the node we're currently on.
    def get_current_node(self):

        return self.nodes.get(
            self.current_node_id
        )

    # Move to the selected dialogue option.
    def choose(self, choice_key):

        current = self.get_current_node()

        if not current:
            return None

        choice_key = str(
            choice_key
        ).strip()

        if choice_key not in current.options:

            return None

        _, next_node_id = (
            current.options[
                choice_key
            ]
        )

        self.current_node_id = (
            next_node_id
        )

        return self.get_current_node()

    # Start the conversation again.
    def reset(self):

        self.current_node_id = (
            self.start_node_id
        )


class NPC:

    def __init__(
        self,
        name,
        description,
        dialogue_tree
    ):
        self.name = name
        self.description = description
        self.dialogue_tree = dialogue_tree

    # Reset before talking to the NPC.
    def start_conversation(self):

        self.dialogue_tree.reset()

        return (
            self.dialogue_tree
            .get_current_node()
        )

    # Pick a dialogue option.
    def say(self, choice_key):

        return (
            self.dialogue_tree
            .choose(choice_key)
        )


def create_ernest_dialogue():
    """
    Ernest - drunken fellow.
    """

    tree = DialogueTree(
        start_node_id="greeting"
    )

    greeting = DialogueNode(
        "greeting",
        (
            "Ernest: What brings you here?\n"
        )
    )

    greeting.options = {
        "1": (
            "Tell me about the dungeon to the east",
            "ashenhollow_info"
        ),

        "2": (
            "Say Nothing and Leave",
            "end"
        )
    }

    tree.add_node(
        greeting
    )

    ashenhollow_info = DialogueNode(
        "ashenhollow_info",
        (
            "Ernest: Ashenhollow? "
            "That dungeon is dangerous, friend.\n"
            "Creatures there are vicious. "
            "But the loot... if you're brave enough.\n"
            "Just be careful of the at the end, "
            "there is a dangerous enemy there."
        )
    )

    ashenhollow_info.options = {
        "1": (
            "Thanks",
            "end"
        ),

        "2": (
            "Say Nothing",
            "end"
        )
    }

    tree.add_node(
        ashenhollow_info
    )

    # Empty node used to end the chat.
    end = DialogueNode(
        "end",
        "  "
    )

    end.options = {}

    tree.add_node(
        end
    )

    return tree
def create_soldat_dialogue():
    """
    Soldat Vanderbilt - Commander of the Northern Expedition.
    """

    tree = DialogueTree(
        start_node_id="greeting"
    )

    greeting = DialogueNode(
        "greeting",
        (
            "Soldat: Hm. You again.\n"
            "I remember you. You're the one who made it "
            "past my men and nearly made a corpse out of me.\n"
            "Didn't expect to see you standing here "
            "in Anatoli."
        )
    )

    greeting.options = {
        "1": (
            "You were the one who attacked me.",
            "confrontation"
        ),

        "2": (
            "Tell me about your expedition.",
            "expedition"
        ),

        "3": (
            "Do you block dungeons?",
            "dungeons"
        ),

        "4": (
            "I'll be going.",
            "end"
        )
    }

    tree.add_node(
        greeting
    )

    confrontation = DialogueNode(
        "confrontation",
        (
            "Soldat: I did what I had to do.\n"
            "The northern routes aren't some tourist trail. "
            "My orders are to keep people from wandering into places "
            "they don't understand.\n"
            "You looked like another fool who thought "
            "swinging a sword was enough to survive up here.\n"
            "Apparently, I was wrong about you."
        )
    )

    confrontation.options = {
        "1": (
            "So you admit I proved you wrong?",
            "respect"
        ),

        "2": (
            "You could have just talked to me.",
            "dense_response"
        ),

        "3": (
            "Tell me about the northern expedition.",
            "expedition"
        )
    }

    tree.add_node(
        confrontation
    )

    respect = DialogueNode(
        "respect",
        (
            "Soldat: Don't get ahead of yourself.\n"
            "You defeated me. That's all.\n"
            "Still... anyone who can get through a "
            "commander of the northern expedition has earned "
            "the right to walk these mountains."
        )
    )

    respect.options = {
        "1": (
            "Fair enough.",
            "end"
        ),

        "2": (
            "What are you protecting up here?",
            "expedition"
        )
    }

    tree.add_node(
        respect
    )

    dense_response = DialogueNode(
        "dense_response",
        (
            "Soldat: Talk?\n"
            "I did talk.\n"
            "I told you to stop.\n"
            "You didn't.\n"
            "Therefore, we fought.\n"
            "Seems pretty straightforward to me."
        )
    )

    dense_response.options = {
        "1": (
            "You're surprisingly bad at explaining yourself.",
            "respect"
        ),

        "2": (
            "Never mind.",
            "end"
        )
    }

    tree.add_node(
        dense_response
    )

    expedition = DialogueNode(
        "expedition",
        (
            "Soldat: I'm the commander of the northern expedition squad.\n"
            "I've got roughly ten men under my command.\n"
            "We patrol the northern routes, map the mountains,\n "
            "and keep watch over the things that crawl out of the \n"
            "dungeons."
            "Most of my men are good soldiers. A few are idiots.\n"
            "Usually the idiots are the ones who volunteer\n "
            "to go first."
        )
    )

    expedition.options = {
        "1": (
            "What are you looking for?",
            "watcher"
        ),

        "2": (
            "Why are the dungeons so dangerous?",
            "dungeons"
        ),

        "3": (
            "Sounds like a miserable job.",
            "commander"
        )
    }

    tree.add_node(
        expedition
    )

    watcher = DialogueNode(
        "watcher",
        (
            "Soldat: Information, mostly.\n"
            "The mountains don't behave like normal land.\n"
            "Strange weather. Strange creatures. Strange ruins.\n"
            "And then there's the thing at the top.\n"
            "The old stories say something sleeps above\n "
            "the clouds."
            "I don't believe old stories.\n"
            "But I also don't climb mountains for fun."
        )
    )

    watcher.options = {
        "1": (
            "You mean the being at the peak of Anatoli?",
            "anatoli"
        ),

        "2": (
            "What happens if someone reaches it?",
            "anatoli"
        ),

        "3": (
            "I'll find out myself.",
            "end"
        )
    }

    tree.add_node(
        watcher
    )

    anatoli = DialogueNode(
        "anatoli",
        (
            "Soldat: That's the problem.\n"
            "Everyone who comes here thinks they're the one "
            "who can handle it.\n"
            "Anatoli has buried stronger men than you and me.\n"
            "If you intend to keep going north, don't mistake\n "
            "surviving one fight for being prepared.\n"
            "The higher you climb, the less the world behaves\n "
            "the way it should."
        )
    )

    anatoli.options = {
        "1": (
            "Then why stay here?",
            "stay"
        ),

        "2": (
            "I'll take my chances.",
            "respect"
        ),

        "3": (
            "Tell me about the dungeons.",
            "dungeons"
        )
    }

    tree.add_node(
        anatoli
    )

    dungeons = DialogueNode(
        "dungeons",
        (
            "Soldat: Because the dungeons aren't empty.\n"
            "My squad has encountered things down there "
            "that shouldn't exist in the first place.\n"
            "That's why we sometimes stop travelers from "
            "going deeper.\n"
            "If you see my men blocking a dungeon, "
            "don't take it personally.\n"
            "We're trying to keep people alive.\n"
            "Usually."
        )
    )

    dungeons.options = {
        "1": (
            "Usually?",
            "dense_response"
        ),

        "2": (
            "What if I want to go anyway?",
            "challenge"
        ),

        "3": (
            "I understand.",
            "end"
        )
    }

    tree.add_node(
        dungeons
    )

    challenge = DialogueNode(
        "challenge",
        (
            "Soldat: Then you'll probably fight one of my men.\n"
            "Or me, if you're unlucky.\n"
            "Though you've already beaten me once, "
            "so perhaps I should stop making that threat."
        )
    )

    challenge.options = {
        "1": (
            "Good idea.",
            "respect"
        ),

        "2": (
            "I won't let you stop me.",
            "end"
        )
    }

    tree.add_node(
        challenge
    )

    commander = DialogueNode(
        "commander",
        (
            "Soldat: Miserable? No.\n"
            "Cold? Yes.\n"
            "Dangerous? Constantly.\n"
            "Underpaid? Absolutely.\n"
            "But these men follow me because they know "
            "I'll never ask them to do something I wouldn't do myself.\n"
            "Even if some of them are idiots."
        )
    )

    commander.options = {
        "1": (
            "You seem to care about your squad.",
            "respect"
        ),

        "2": (
            "I'll leave you to your command.",
            "end"
        )
    }

    tree.add_node(
        commander
    )

    stay = DialogueNode(
        "stay",
        (
            "Soldat: Someone has to.\n"
            "Anatoli is my home. These mountains are my "
            "responsibility.\n"
            "Also I've found this note that says "
            "'Password'\n"
            "I don't really know what to say? "
            "But anyway."
        )
    )

    stay.options = {
        "1": (
            "Good luck, Commander.",
            "end"
        ),

        "2": (
            "I'll see you around.",
            "end"
        )
    }

    tree.add_node(
        stay
    )

    end = DialogueNode(
        "end",
        "Soldat: Stay alive, Exiled. The north isn't finished with you yet."
    )

    end.options = {}

    tree.add_node(
        end
    )

    return tree


def create_mary_dialogue():
    """
    Mary - mysterious.
    """

    tree = DialogueTree(
        start_node_id="greeting"
    )

    greeting = DialogueNode(
        "greeting",
        (
            "Mary Althea: Greetings. Traveller from beyond "
            "the sky. I am Mary. I offer you an accord..\n"
            "I sense you are destined for great trials ahead.\n"
            "Desirest thou required further knowledge?"
        )
    )

    greeting.options = {
        "1": (
            "Please continue",
            "dungeons_warning"
        ),

        "2": (
            "No thanks",
            "end"
        )
    }

    tree.add_node(
        greeting
    )

    dungeons_warning = DialogueNode(
        "dungeons_warning",
        (
            "Mary: First be warned about the dungeon "
            "to the east and west.\n"
            "Those who venture into them must be prepared.\n"
            "I left a dagger at the entry outside you "
            "should be able to get it."
        )
    )

    dungeons_warning.options = {
        "1": (
            "Thank you",
            "end"
        ),

        "2": (
            "Say Nothing",
            "end"
        )
    }

    tree.add_node(
        dungeons_warning
    )

    # End the conversation here.
    end = DialogueNode(
        "end",
        "  "
    )

    end.options = {}

    tree.add_node(
        end
    )

    return tree
