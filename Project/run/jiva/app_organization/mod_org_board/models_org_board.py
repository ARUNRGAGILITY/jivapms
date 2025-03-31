
from app_organization.mod_app.all_model_imports import *
from app_organization.mod_organization.models_organization import *
from app_organization.mod_project.models_project import *   
from app_common.mod_common.models_common import *
from app_organization.mod_project_board.models_project_board import *
from app_organization.mod_project_board_state.models_project_board_state import *
from app_organization.mod_project_board_swimlane.models_project_board_swimlane import *
from app_jivapms.mod_app.all_view_imports import *
from app_common.mod_app.all_view_imports import *

class OrgBoard(BaseModelImpl):
    org = models.ForeignKey('app_organization.Organization', on_delete=models.CASCADE, 
                            related_name="org_boards", null=True, blank=True)
    
    project = models.ForeignKey('app_organization.Project', on_delete=models.CASCADE, 
                                related_name="org_project_boards", null=True, blank=True)
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_org_boards")
   
        
    def __str__(self):
        if self.name:
            return self.name
        else:
            return str(self.id)


class ProjectBoardCard(BaseModelTrackDateImpl):
    backlog = models.ForeignKey('app_organization.Backlog', on_delete=models.CASCADE, related_name="board_cards", null=True, blank=True)    
    board = models.ForeignKey(ProjectBoard, on_delete=models.CASCADE, related_name="board_cards", null=True, blank=True)
    state = models.ForeignKey(ProjectBoardState, on_delete=models.CASCADE, related_name="state_cards", null=True, blank=True)
    swimlane = models.ForeignKey(
        'app_organization.ProjectBoardSwimLane', on_delete=models.SET_NULL, null=True, blank=True, related_name="swimlane_cards"
    )
    SUBSTATE_CHOICE = [
        ('Doing', 'Doing'),
        ('Done', 'Done'),
        ('MVP', 'MVP'),
        ('Persevere', 'Persevere'),
        ('In-Progress', 'In-Progress'),
        ('Ready', 'Ready'),
    ]
    substate = models.CharField(max_length=50, choices=SUBSTATE_CHOICE, default='Doing')
    class Meta:
        indexes = [
            models.Index(fields=['board', 'state']),
        ]
    def __str__(self):
        # if self.backlog != None and self.backlog.name:
        #     return self.backlog.name
        # else:
        #     return str(self.id)
        
        return f"{self.backlog} {self.backlog.id}"



class ProjectBoardStateTransition(BaseModelTrackDateImpl):
    date_field = models.DateField(null=True, blank=True)  # Separate date field
    time_field = models.TimeField(null=True, blank=True)  # Separate time field
    
    board = models.ForeignKey('app_organization.ProjectBoard', on_delete=models.CASCADE, related_name="board_transitions", null=True, blank=True)
    card = models.ForeignKey('app_organization.Backlog', on_delete=models.CASCADE,null=True, blank=True,
                               related_name="card_transitions")
                           

    from_state = models.ForeignKey(
        'app_organization.ProjectBoardState',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transitions_from"
    )
    to_state = models.ForeignKey(
        'app_organization.ProjectBoardState',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transitions_to"
    )
    transition_time = models.DateTimeField(auto_now_add=True, null=True,
        blank=True)
    
    triggered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # User who moved the card
    notes = models.TextField(null=True, blank=True)  # Optional transition notes

    # def __str__(self):
    #     return f"Transition of Card {self.card.id}: {self.from_state} → {self.to_state} at {self.transition_time}"
    def save(self, *args, **kwargs):
        if self.transition_time:  # Convert date_time to IST
            ist_date_time = self.transition_time.astimezone(IST)
            self.date_field = ist_date_time.date()  # Store date in YYYY-MM-DD format
            # Remove microseconds from the time
            ist_time = ist_date_time.time()
            self.time_field = time(ist_time.hour, ist_time.minute)  
        super().save(*args, **kwargs)

    def formatted_date(self):
        return self.date_field.strftime('%d-%m-%Y') if self.date_field else None

    def formatted_time(self):
        return self.time_field.strftime('%H:%M') if self.time_field else None

    def __str__(self):
        if self.card.id:
            return f"CARD_MOVEMENT: {self.formatted_date()} {self.formatted_time()} - {self.card.id}: {self.from_state} → {self.to_state}"
        else:
            return f"NEW_CARD_MOVEMENT: {self.formatted_date()} {self.formatted_time()} - {self.from_state} → {self.to_state}"




class Movement(BaseModelTrackDateImpl):
    date_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    date = models.DateField(null=True, blank=True)  # Separate date field
    time = models.TimeField(null=True, blank=True)  # Separate time field
    
    project = models.ForeignKey('app_organization.Project', on_delete=models.CASCADE, related_name="project_movements", null=True, blank=True)
    board = models.ForeignKey('app_organization.ProjectBoard', on_delete=models.CASCADE, related_name="board_movements", null=True, blank=True)
    card = models.ForeignKey('app_organization.Backlog', on_delete=models.CASCADE, null=True, blank=True, related_name="card_movements")

    from_column = models.ForeignKey(
        'app_organization.ProjectBoardState',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="column_froms"
    )
    to_column = models.ForeignKey(
        'app_organization.ProjectBoardState',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="column_tos"
    )
    triggered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # User who moved the card

    def save(self, *args, **kwargs):
        if self.date_time:  # Convert date_time to IST
            ist_date_time = self.date_time.astimezone(IST)
            self.date = ist_date_time.date()  # Store date in YYYY-MM-DD format
            self.time = ist_date_time.time()  # Store time in HH:MM:SS format
        super().save(*args, **kwargs)

    def formatted_date(self):
        return self.date.strftime('%d-%m-%Y') if self.date else None

    def formatted_time(self):
        return self.time.strftime('%H:%M:%S') if self.time else None

    def __str__(self):
        return f"CARD_MOVEMENT: {self.formatted_date()} {self.formatted_time()} - {self.card.id}: {self.from_column} → {self.to_column}"



class ProjectBoardCardManager(models.Manager):
    def calculate_story_points(self, board, state_names, iteration_backlog_items):
        # Fetch states by their names
        states = {}
        for name in state_names:
            states[name] = ProjectBoardState.objects.filter(name=name, active=True).values_list('id', flat=True)

        # Log states for debugging
        logger.debug(f"States: {states}")

        # Fetch ProjectBoardCards linked to these states
        backlog_ids = {state: ProjectBoardCard.objects.filter(
            board=board, state_id__in=states[state], active=True
        ).values_list('backlog_id', flat=True) for state in state_names}

        # Log backlog IDs for debugging
        logger.debug(f"Backlog IDs: {backlog_ids}")

        # Check done cards for non-numeric or invalid sizes
        if "Done" in backlog_ids:
            done_cards = ProjectBoardCard.objects.filter(board=board, state_id__in=states["Done"], active=True)
            for card in done_cards:
                if card.backlog and isinstance(card.backlog.size, int):
                    logger.debug(f"Done Card: {card.backlog.id} {card.backlog.size}")
                else:
                    logger.debug(f"Done Card: {card.backlog.id} {card.backlog.size} {type(card.backlog.size)}")

        # Calculate story points for each state
        story_points = {}
        for state, ids in backlog_ids.items():
            story_points[state] = iteration_backlog_items.filter(id__in=ids).aggregate(total=Sum('size'))['total'] or 0

        # Log calculated story points
        logger.debug(f"Story Points: {story_points}")

        return story_points
