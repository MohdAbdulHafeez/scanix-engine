class ConfidenceEngine:

    @staticmethod
    def score(

        evidence_count,
        passed

    ):

        if passed:

            if evidence_count == 0:

                return 95

            return 90

        if evidence_count >= 3:

            return 99

        if evidence_count >= 1:

            return 95

        return 70