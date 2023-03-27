from datetime import datetime, timezone

from django.utils.translation import gettext_lazy as _
from django_transitions.workflow import StatusBase, StateMachineMixinBase
from transitions import Machine


class CandidateStatus(StatusBase):
    RECORD_CREATED = 'record_created'
    RECORD_COMPLETED = 'record_completed'
    RECORD_ACCEPTED = 'record_accepted'
    MEETING_PROPOSED = 'meeting_proposed'
    WAITING_MEETING = 'waiting_meeting'
    WAITING_CANDIDATE = 'waiting_candidate'
    CANDIDATE_CONFIRMED = 'candidate_confirmed'
    REJECTED = 'rejected'
    WAITING_CREATION = 'waiting_creation'
    WAITING_TRAINING = 'waiting_training'
    CLOSURE = 'closure'

    STATE_CHOICES = (
        (RECORD_CREATED, _("Dossier créé")),
        (RECORD_COMPLETED, _("Dossier complété")),
        (RECORD_ACCEPTED, _("Dossier complet")),
        (MEETING_PROPOSED, _("Date d'entretien proposée")),
        (WAITING_MEETING, _("En attente de l'entretien")),
        (WAITING_CANDIDATE, _("En attente de retour du candidat")),
        (CANDIDATE_CONFIRMED, _("En attente de retour du recrutement")),
        (REJECTED, _("Candidature refusée")),
        (WAITING_CREATION, _("En attente de la création des accès")),
        (WAITING_TRAINING, _("En attente de l'ajout des compétences")),
        (CLOSURE, _("Dossier clôturé")),
    )

    RECORD_COMPLETION = "record_completion"
    RECORD_REJECTION = "record_rejection"
    RECORD_ACCEPTION = "record_acception"
    MEETING_PROPOSITION = "meeting_proposition"
    MEETING_REJECTION = "meeting_rejection"
    MEETING_ACCEPTION = "meeting_acception"
    MEETING_ABSENCE = "meeting_absence"
    MEETING_PRESENCE = "meeting_presence"
    CANDIDATE_RESIGNATION = "candidate_resignation"
    RECRUITER_REJECTION = "candidate_rejection"
    CANDIDATE_CONFIRMATION = "candidate_confirmation"
    RECRUITER_ACCEPTION = "candidate_acception"
    ACCOUNT_CREATION = "account_creation"
    CLOSING = "closing"
    DESTRUCTION = "destruction"

    TRANSITION_LABELS = {
        RECORD_COMPLETION: {'label': _("Marquer comme complet")},
        RECORD_REJECTION: {'label': _("Marquer comme incomplet")},
        RECORD_ACCEPTION: {'label': _("Accepter le dossier")},
        MEETING_PROPOSITION: {'label': _("Proposer un entretien")},
        MEETING_REJECTION: {'label': _("Refuser la date d'entretien")},
        MEETING_ACCEPTION: {'label': _("Accepter la date d'entretien")},
        MEETING_ABSENCE: {'label': _("Absent à l'entretien")},
        MEETING_PRESENCE: {'label': _("Présent à l'entretien")},
        CANDIDATE_RESIGNATION: {'label': _("Renoncer à la candidature")},
        RECRUITER_REJECTION: {'label': _("Rejeter la candidature")},
        CANDIDATE_CONFIRMATION: {'label': _("Confirmer la candidature")},
        RECRUITER_ACCEPTION: {'label': _("Accepter la candidature")},
        ACCOUNT_CREATION: {'label': _("Compte créé")},
        CLOSING: {'label': _("Clôre le dossier")},
        DESTRUCTION: {'label': _("Destruction du dossier")},
    }

    SM_STATES = [RECORD_CREATED, RECORD_COMPLETED, RECORD_ACCEPTED, MEETING_PROPOSED, WAITING_MEETING, WAITING_CANDIDATE,
                 CANDIDATE_CONFIRMED, REJECTED, WAITING_CREATION, WAITING_TRAINING, CLOSURE]
    SM_INITIAL_STATE = RECORD_CREATED

    SM_TRANSITIONS = [
        {
            'trigger': RECORD_COMPLETION,
            'source': [RECORD_CREATED],
            'dest': RECORD_COMPLETED
        },
        {
            'trigger': RECORD_REJECTION,
            'source': [RECORD_COMPLETED],
            'dest': RECORD_CREATED
        },
        {
            'trigger': RECORD_ACCEPTION,
            'source': [RECORD_COMPLETED],
            'dest': RECORD_ACCEPTED
        },
        {
            'trigger': MEETING_PROPOSITION,
            'source': [RECORD_ACCEPTED],
            'dest': MEETING_PROPOSED
        },
        {
            'trigger': MEETING_REJECTION,
            'source': [MEETING_PROPOSED],
            'dest': RECORD_ACCEPTED
        },
        {
            'trigger': MEETING_ACCEPTION,
            'source': [MEETING_PROPOSED],
            'dest': WAITING_MEETING
        },
        {
            'trigger': MEETING_ABSENCE,
            'source': [WAITING_MEETING],
            'dest': RECORD_ACCEPTED
        },
        {
            'trigger': MEETING_PRESENCE,
            'source': [WAITING_MEETING],
            'dest': WAITING_CANDIDATE
        },
        {
            'trigger': CANDIDATE_RESIGNATION,
            'source': [WAITING_CANDIDATE],
            'dest': CLOSURE
        },
        {
            'trigger': CANDIDATE_CONFIRMATION,
            'source': [WAITING_CANDIDATE],
            'dest': CANDIDATE_CONFIRMED
        },
        {
            'trigger': RECRUITER_ACCEPTION,
            'source': [CANDIDATE_CONFIRMED],
            'dest': WAITING_CREATION
        },
        {
            'trigger': RECRUITER_REJECTION,
            'source': [CANDIDATE_CONFIRMED],
            'dest': REJECTED
        },
        {
            'trigger': ACCOUNT_CREATION,
            'source': [WAITING_CREATION],
            'dest': WAITING_TRAINING
        },

    ]


class CandidateStateMachineMixin(StateMachineMixinBase):
    """Lifecycle workflow state machine."""

    status_class = CandidateStatus

    machine = Machine(
        model=None,
        finalize_event='wf_finalize',
        auto_transitions=False,
        **status_class.get_kwargs()  # noqa: C815
    )

    @property
    def state(self):
        """Get the items workflowstate or the initial state if none is set."""
        if self.status:
            return self.status
        return self.machine.initial

    @state.setter
    def state(self, value):
        """Set the items workflow state."""
        self.status = value

    def wf_finalize(self, *args, **kwargs):
        """Run this on all transitions."""
        self.update = datetime.now(timezone.utc)
