from django.db import models

# Create your models here.

class User(models.Model):
    # creating roles for a user as an enum type
    class Role(models.TextChoices):
        CLIENT = 'CLIENT', 'Client'
        ADMIN = 'ADMIN', 'Admin'
    
    
    username = models.CharField(max_length=128)
    email = models.EmailField(max_length=32)
    password_hash = models.CharField(max_length=256)
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.CLIENT
    )
    
    def __str__(self):
        """
        method that will be run when User is to be printed
        """
        return f"{self.username} ({self.role})"

# creating the Poll model
class Poll(models.Model):
    creater_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='polls')
    poll_name = models.CharField(max_length=124)
    question = models.TextField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)
    expiring_date = models.DateField(help_text="Date when poll expires")
    is_active = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        """
        method that will be run when Poll is to be printed
        """
        return f"{self.poll_name} created by {self.creater_by} at {self.created_at} expires at {self.expiring_date}"

# creating the VoteOption Model
class VoteOption(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, unique=True, related_name='vote_options')
    option_name = models.CharField(max_length=512, unique=True)
    description = models.TextField(max_length=1024)
    
    def __str__(self) -> str:
        """
        Method to be called when an object of VoteOption is to be created
        """
        return f"{self.poll}: {self.option_name}" 

class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registrations')
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='registrations')
    registered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'poll')  # Ensures one registration per user per poll
        verbose_name = 'Poll Registration'
        verbose_name_plural = 'Poll Registrations'
        db_table = 'poll_registrations'
    
    def __str__(self) -> str:
        """
        method to be called when a registration instance is to be printed
        """
        return f"{self.user.username} registered for {self.poll.poll_name} at {self.registered_at}"
    
    
class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='votes')
    vote_option = models.ForeignKey(VoteOption, on_delete=models.CASCADE, related_name='votes')
    casted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'poll')  # Ensures one vote per user per poll
        verbose_name = 'Vote'
        verbose_name_plural = 'Votes'
        db_table = 'votes'
        ordering = ['-casted_at']
    
    def __str__(self) -> str:
        return f"{self.user.username} voted for {self.vote_option.option_name} in {self.poll.poll_name}"

