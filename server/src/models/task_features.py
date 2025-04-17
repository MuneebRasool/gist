# from tortoise import fields, models
#  from uuid import UUID


#  class TaskUtilityFeatures(models.Model):
#      """
#      Model to store utility features for tasks
#      """
#      id = fields.UUIDField(pk=True)
#      task = fields.ForeignKeyField('models.Task', related_name='utility_features')
#      priority = fields.CharField(max_length=50, null=True)  # high|medium|low
#      deadline_time = fields.CharField(max_length=100, null=True)
#      intrinsic_interest = fields.CharField(max_length=50, null=True)  # high|moderate|low
#      user_personalization = fields.CharField(max_length=50, null=True)  # important|standard
#      task_type_relevance = fields.CharField(max_length=50, null=True)  # high|medium|low
#      emotional_salience = fields.CharField(max_length=50, null=True)  # strong|weak
#      user_feedback = fields.CharField(max_length=50, null=True)  # emphasized|standard
#      domain_relevance = fields.CharField(max_length=50, null=True)  # high|low
#      novel_task = fields.CharField(max_length=50, null=True)  # high|low
#      reward_pathways = fields.CharField(max_length=50, null=True)  # yes|no
#      social_collaborative_signals = fields.CharField(max_length=50, null=True)  # yes|no
#      time_of_day_alignment = fields.CharField(max_length=50, null=True)  # appropriate|inappropriate
#      created_at = fields.DatetimeField(auto_now_add=True)
#      updated_at = fields.DatetimeField(auto_now=True)

#      class Meta:
#          table = "task_utility_features"


#  class TaskCostFeatures(models.Model):
#      """
#      Model to store cost features for tasks
#      """
#      id = fields.UUIDField(pk=True)
#      task = fields.ForeignKeyField('models.Task', related_name='cost_features')
#      task_complexity = fields.CharField(max_length=50, null=True)  # high|medium|low
#      spam_probability = fields.CharField(max_length=50, null=True)  # high|medium|low
#      time_required = fields.FloatField(null=True)  # specific time estimate in hours
#      emotional_stress_factor = fields.CharField(max_length=50, null=True)  # high|medium|low
#      location_dependencies = fields.CharField(max_length=50, null=True)  # count|none
#      key_friction_factors = fields.TextField(null=True)  # Brief explanation of main factors
#      created_at = fields.DatetimeField(auto_now_add=True)
#      updated_at = fields.DatetimeField(auto_now=True)

#      class Meta:
#          table = "task_cost_features"
