import enum
from datetime import datetime, timezone

from django.utils.translation import gettext_lazy as _
from django_transitions.workflow import StatusBase, StateMachineMixinBase
from transitions import Machine


class CandidateStatus(StatusBase):

    class States(enum.Enum):
        RECORD_CREATED = _("Dossier créé")
        RECORD_COMPLETED = _("Dossier complété")
        RECORD_ACCEPTED = _("Dossier complet")
        MEETING_PROPOSED = _("Date d'entretien proposée")
        WAITING_MEETING = _("En attente de l'entretien")
        WAITING_CANDIDATE = _("En attente de retour du candidat")
        CANDIDATE_CONFIRMED = _("En attente de retour du recrutement")
        REJECTED = _("Candidature refusée")
        WAITING_CREATION = _("En attente de la création des accès")
        WAITING_TRAINING = _("En attente de l'ajout des compétences")
        CLOSURE = _("Dossier clôturé")

    STATE_CHOICES = [(state.name, state.value) for state in States]

    # Transitions label
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

    permissions = {transition: label['label'] for transition, label in TRANSITION_LABELS.items()}

    SM_STATES = States
    SM_INITIAL_STATE = States.RECORD_CREATED

    SM_TRANSITIONS = [
        {
            'trigger': RECORD_COMPLETION,
            'source': [States.RECORD_CREATED],
            'dest': States.RECORD_COMPLETED,
        },
        {
            'trigger': RECORD_REJECTION,
            'source': [States.RECORD_COMPLETED],
            'dest': States.RECORD_CREATED,
        },
        {
            'trigger': RECORD_ACCEPTION,
            'source': [States.RECORD_COMPLETED],
            'dest': States.RECORD_ACCEPTED,
        },
        {
            'trigger': MEETING_PROPOSITION,
            'source': [States.RECORD_ACCEPTED],
            'dest': States.MEETING_PROPOSED,
        },
        {
            'trigger': MEETING_REJECTION,
            'source': [States.MEETING_PROPOSED],
            'dest': States.RECORD_ACCEPTED,
        },
        {
            'trigger': MEETING_ACCEPTION,
            'source': [States.MEETING_PROPOSED],
            'dest': States.WAITING_MEETING,
        },
        {
            'trigger': MEETING_ABSENCE,
            'source': [States.WAITING_MEETING],
            'dest': States.RECORD_ACCEPTED,
        },
        {
            'trigger': MEETING_PRESENCE,
            'source': [States.WAITING_MEETING],
            'dest': States.WAITING_CANDIDATE,
        },
        {
            'trigger': CANDIDATE_RESIGNATION,
            'source': [States.WAITING_CANDIDATE],
            'dest': States.CLOSURE,
        },
        {
            'trigger': CANDIDATE_CONFIRMATION,
            'source': [States.WAITING_CANDIDATE],
            'dest': States.CANDIDATE_CONFIRMED,
        },
        {
            'trigger': RECRUITER_ACCEPTION,
            'source': [States.CANDIDATE_CONFIRMED],
            'dest': States.WAITING_CREATION,
        },
        {
            'trigger': RECRUITER_REJECTION,
            'source': [States.CANDIDATE_CONFIRMED],
            'dest': States.REJECTED,
        },
        {
            'trigger': ACCOUNT_CREATION,
            'source': [States.WAITING_CREATION],
            'dest': States.WAITING_TRAINING,
        },
        {
            'trigger': CLOSING,
            'source': [States.REJECTED, States.WAITING_CREATION, States.WAITING_TRAINING],
            'dest': States.CLOSURE,
        },
    ]


class CandidateStateMachineMixin(StateMachineMixinBase):
    """Lifecycle workflow state machine."""

    status_class = CandidateStatus

    machine = Machine(
        model=None,
        finalize_event='wf_finalize',
        auto_transitions=False,
        initial=CandidateStatus.SM_INITIAL_STATE,
        states=CandidateStatus.SM_STATES,
        transitions=CandidateStatus.SM_TRANSITIONS
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
