__all__ = ['ground', 'get_models', 'get_names']

from gilda.grounder import Grounder


class GrounderInstance(object):
    def __init__(self):
        self.grounder = None

    def get_grounder(self):
        if self.grounder is None:
            self.grounder = Grounder()
        return self.grounder

    def ground(self, text, context=None):
        _grounder = self.get_grounder()
        scored_matches = _grounder.ground(text)
        if context:
            scored_matches = _grounder.disambiguate(text,
                                                    scored_matches,
                                                    context)
        scored_matches = sorted(scored_matches, key=lambda x: x.score,
                                reverse=True)
        return scored_matches

    def get_models(self):
        return sorted(list(self.get_grounder().gilda_disambiguators.keys()))

    def get_names(self, db, id, status=None, source=None):
        names = []
        for entries in self.get_grounder().entries.values():
            for entry in entries:
                if (entry.db == db) and (entry.id == id) and \
                        (not status or entry.status == status) and \
                        (not source or entry.source == source):
                    names.append(entry.text)
        return sorted(list(set(names)))


grounder = GrounderInstance()


def ground(text, context=None):
    """Return a list of scored matches for a text to ground.

    Parameters
    ----------
    text : str
        The entity text to be grounded.
    context : Optional[str]
        Any additional text that serves as context for disambiguating the
        given entity text, used if a model exists for disambiguating the
        given text.

    Returns
    -------
    list[gilda.grounder.ScoredMatch]
        A list of ScoredMatch objects representing the groundings.
    """
    return grounder.ground(text=text, context=context)


def get_models():
    """Return a list of entity texts for which disambiguation models exist.

    Returns
    -------
    list[str]
        The list of entity texts for which a disambiguation model is
        available.
    """
    return grounder.get_models()


def get_names(db, id, status=None, source=None):
    """Return a list of entity texts corresponding to a given database ID.

    Parameters
    ----------
    db : str
        The database in which the ID is an entry, e.g., HGNC.
    id : str
        The ID of an entry in the database.
    status : Optional[str]
        If given, only entity texts with the given status e.g., "synonym"
        are returned.
    source : Optional[str]
        If given, only entity texts from the given source e.g., "uniprot"
        are returned.
    """
    return grounder.get_names(db, id, status=status, source=source)
