from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm, Form
from django.forms import ModelChoiceField
from datetime import datetime

class CommitteeBudget(models.Model):
    """
    Model for the budget of a specific committee
    """
    name = models.TextField()
    start_budget = models.PositiveIntegerField(default=0)
    current_budget = models.positiveIntegerField(default=0)
    expenses = models.ForeignKey(Expense)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def total_expenses(self):
        return sum([e.amount for e in self.expenses])

    class Meta:
        verbose_name = "Budget"
        verbost_name_plural = "Budgets"

class Expense(models.Model):
    """
    Model for an expense of a committee
    """
    amount = models.IntegerField()
    name = models.TextField()
    description = models.TextField()
    source = models.TextField()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"
