from collections import (
    deque
)

from datetime import (
    datetime
)

from uuid import (
    uuid4
)

import os


class ConversationMemory:

    def __init__(

        self,

        session_id=None,

        max_messages=None,

        max_products=25

    ):

        self.session_id = (

            session_id

            or

            str(
                uuid4()
            )

        )

        self.max_messages = (

            max_messages

            or

            int(

                os.getenv(

                    "AGENT_MEMORY_SIZE",

                    30

                )

            )

        )

        self.max_products = (
            max_products
        )

        self.messages = (

            deque(

                maxlen=self.max_messages

            )

        )

        self.product_history = (

            deque(

                maxlen=max_products

            )

        )

        self.user_profile = {

            "goal": None,

            "diet": None,

            "allergies": [],

            "medical_conditions": [],

            "preferences": [],

            "activity_level": None,

            "age": None,

            "gender": None

        }

        self.agent_state = {

            "last_product": None,

            "last_recommendation": None,

            "last_risk_level": None

        }

    # =====================================
    # SESSION
    # =====================================

    def get_session_id(

        self

    ):

        return self.session_id

    # =====================================
    # USER PROFILE
    # =====================================

    def update_profile(

        self,

        **kwargs

    ):

        for key, value in kwargs.items():

            if key in self.user_profile:

                self.user_profile[
                    key
                ] = value

    def get_profile(

        self

    ):

        return self.user_profile

    # =====================================
    # PRODUCT MEMORY
    # =====================================

    def add_product(

        self,

        product_name,

        summary=None,

        score=None

    ):

        self.product_history.append({

            "product_name":
            product_name,

            "summary":
            summary,

            "score":
            score,

            "timestamp":

            datetime.utcnow()

            .isoformat()

        })

        self.agent_state[
            "last_product"
        ] = product_name

    def get_products(

        self

    ):

        return list(

            self.product_history

        )

    # =====================================
    # AGENT STATE
    # =====================================

    def update_state(

        self,

        **kwargs

    ):

        for key, value in kwargs.items():

            self.agent_state[
                key
            ] = value

    def get_state(

        self

    ):

        return self.agent_state

    # =====================================
    # CONVERSATION
    # =====================================

    def add_message(

        self,

        role,

        content

    ):

        self.messages.append({

            "role":
            role,

            "content":
            content,

            "timestamp":

            datetime.utcnow()

            .isoformat()

        })

    def get_history(

        self

    ):

        return list(

            self.messages

        )

    # =====================================
    # MEMORY SUMMARY
    # =====================================

    def build_memory_summary(

        self

    ):

        profile = (

            self.get_profile()

        )

        state = (

            self.get_state()

        )

        recent_products = (

            self.get_products()

        )[-5:]

        summary = f"""

SESSION ID:
{self.session_id}

GOAL:
{profile['goal']}

DIET:
{profile['diet']}

ACTIVITY LEVEL:
{profile['activity_level']}

ALLERGIES:
{profile['allergies']}

MEDICAL CONDITIONS:
{profile['medical_conditions']}

PREFERENCES:
{profile['preferences']}

LAST PRODUCT:
{state['last_product']}

LAST RECOMMENDATION:
{state['last_recommendation']}

LAST RISK:
{state['last_risk_level']}

RECENT PRODUCTS:
{recent_products}

"""

        return summary

    # =====================================
    # AGENT CONTEXT
    # =====================================

    def build_context(

        self

    ):

        context = []

        context.append(

            self.build_memory_summary()

        )

        context.append(

            "\n\nRECENT CONVERSATION\n\n"

        )

        recent_messages = (

            list(

                self.messages

            )[-10:]

        )

        for message in recent_messages:

            context.append(

                f"""

{message['role'].upper()}

{message['content']}

"""
            )

        return "\n".join(

            context

        )

    # =====================================
    # RETRIEVAL HELPERS
    # =====================================

    def find_product(

        self,

        product_name

    ):

        for product in reversed(

            self.product_history

        ):

            if (

                product[
                    "product_name"
                ]

                .lower()

                ==

                product_name
                .lower()

            ):

                return product

        return None

    # =====================================
    # RESET
    # =====================================

    def clear_messages(

        self

    ):

        self.messages.clear()

    def clear_products(

        self

    ):

        self.product_history.clear()

    def clear_all(

        self

    ):

        self.messages.clear()

        self.product_history.clear()

        self.agent_state = {

            "last_product": None,

            "last_recommendation": None,

            "last_risk_level": None

        }