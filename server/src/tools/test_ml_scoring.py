# """
#  Test script for ML-based task scoring system
#  """
#  import asyncio
#  from datetime import datetime, timedelta
#  from src.models.task_scoring import scoring_model
#  from src.modules.tasks.service import TaskService
#  from src.modules.tasks.schemas import TaskCreate
#  from src.models.graph.nodes import TaskNode, EmailNode, UserNode
 
#  async def create_test_tasks(user_id: str):
#      """Create sample tasks for testing"""
#      # Create a test email node
#      email_id = "test_email_123"
     
#      # Sample tasks with different priorities and deadlines
#      tasks = [
#          {
#              "title": "Review project proposal",
#              "priority": "high",
#              "deadline": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
#              "utility_features": {"importance": 0.8, "urgency": 0.9},
#              "cost_features": {"time_cost": 0.6, "complexity": 0.7}
#          },
#          {
#              "title": "Schedule team meeting",
#              "priority": "medium",
#              "deadline": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
#              "utility_features": {"importance": 0.6, "urgency": 0.5},
#              "cost_features": {"time_cost": 0.3, "complexity": 0.2}
#          },
#          {
#              "title": "Update documentation",
#              "priority": "low",
#              "deadline": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
#              "utility_features": {"importance": 0.4, "urgency": 0.3},
#              "cost_features": {"time_cost": 0.4, "complexity": 0.3}
#          }
#      ]
     
#      created_tasks = []
#      for task in tasks:
#          # Prepare task data for scoring
#          task_data = {
#              'utility_features': task['utility_features'],
#              'cost_features': task['cost_features'],
#              'priority': task['priority'],
#              'deadline': task['deadline']
#          }
         
#          # Get ML-based score
#          features = scoring_model.extract_features(task_data)
#          ml_score = scoring_model.predict(features)
         
#          # Create task
#          created_task = await TaskService.create_task(
#              task_data=TaskCreate(
#                  task=task["title"],
#                  deadline=task["deadline"],
#                  priority=task["priority"],
#                  messageId=email_id,
#                  relevance_score=ml_score,
#                  utility_score=sum(task["utility_features"].values()) / len(task["utility_features"]),
#                  cost_score=sum(task["cost_features"].values()) / len(task["cost_features"])
#              ),
#              user_id=user_id
#          )
#          created_tasks.append(created_task)
#          print(f"Created task: {task['title']}")
#          print(f"Initial ML score: {ml_score}")
         
#      return created_tasks
 
#  async def simulate_reordering(tasks: list[TaskNode]):
#      """Simulate user reordering tasks"""
#      print("\nSimulating task reordering...")
     
#      # Move "Update documentation" up several times
#      doc_task = next(t for t in tasks if "documentation" in t.task.lower())
#      for _ in range(3):
#          print(f"\nMoving '{doc_task.task}' up")
#          updated_task = await TaskService.reorder_task(doc_task.task_id, "up")
#          print(f"New relevance score: {updated_task.relevance_score}")
#          await asyncio.sleep(1)  # Small delay between operations
     
#      # Move "Review project proposal" down
#      review_task = next(t for t in tasks if "review" in t.task.lower())
#      print(f"\nMoving '{review_task.task}' down")
#      updated_task = await TaskService.reorder_task(review_task.task_id, "down")
#      print(f"New relevance score: {updated_task.relevance_score}")
 
#  async def create_similar_tasks(user_id: str):
#      """Create similar tasks to test learning effect"""
#      print("\nCreating similar tasks to test learning effect...")
     
#      similar_tasks = [
#          {
#              "title": "Review design document",
#              "priority": "high",
#              "deadline": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
#              "utility_features": {"importance": 0.8, "urgency": 0.8},
#              "cost_features": {"time_cost": 0.6, "complexity": 0.7}
#          },
#          {
#              "title": "Update readme files",
#              "priority": "low",
#              "deadline": (datetime.now() + timedelta(days=6)).strftime("%Y-%m-%d"),
#              "utility_features": {"importance": 0.4, "urgency": 0.3},
#              "cost_features": {"time_cost": 0.4, "complexity": 0.3}
#          }
#      ]
     
#      email_id = "test_email_456"
#      for task in similar_tasks:
#          # Prepare task data for scoring
#          task_data = {
#              'utility_features': task['utility_features'],
#              'cost_features': task['cost_features'],
#              'priority': task['priority'],
#              'deadline': task['deadline']
#          }
         
#          # Get ML-based score
#          features = scoring_model.extract_features(task_data)
#          ml_score = scoring_model.predict(features)
         
#          # Create task
#          created_task = await TaskService.create_task(
#              task_data=TaskCreate(
#                  task=task["title"],
#                  deadline=task["deadline"],
#                  priority=task["priority"],
#                  messageId=email_id,
#                  relevance_score=ml_score,
#                  utility_score=sum(task["utility_features"].values()) / len(task["utility_features"]),
#                  cost_score=sum(task["cost_features"].values()) / len(task["cost_features"])
#              ),
#              user_id=user_id
#          )
#          print(f"\nCreated similar task: {task['title']}")
#          print(f"ML score: {ml_score}")
 
#  async def main():
#      """Main test function"""
#      # Use a test user ID
#      test_user_id = "test_user_123"
     
#      try:
#          # Ensure test user exists
#          try:
#              user_node = UserNode.nodes.get(userid=test_user_id)
#          except UserNode.DoesNotExist:
#              user_node = UserNode(userid=test_user_id).save()
         
#          print("Creating initial test tasks...")
#          tasks = await create_test_tasks(test_user_id)
         
#          # Wait a bit to simulate user interaction
#          await asyncio.sleep(2)
         
#          # Simulate reordering
#          await simulate_reordering(tasks)
         
#          # Wait to let the model process the feedback
#          await asyncio.sleep(2)
         
#          # Create similar tasks to test learning
#          await create_similar_tasks(test_user_id)
         
#          print("\nTest completed successfully!")
         
#      except Exception as e:
#          print(f"Error during testing: {str(e)}")
 
#  if __name__ == "__main__":
#      asyncio.run(main())