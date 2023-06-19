from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from tasks.models import ToDo

class ToDoModelTestCase(TestCase):
    def setUp(self):
        self.todo = ToDo.objects.create(
            user_name="User Name",
            task="Sample Task",
            description="Sample Description",
            status="Pending",
            file=None,
        )

    def test_todo_fields(self):
        self.assertEqual(self.todo.user_name, "User Name")
        self.assertEqual(self.todo.task, "Sample Task")
        self.assertEqual(self.todo.description, "Sample Description")
        self.assertEqual(self.todo.status, "Pending")
        self.assertEqual(self.todo.file,None)

    def test_default_status(self):
        todo = ToDo.objects.create(user_name="JaneDoe", task="Another Task")
        self.assertEqual(todo.status, "Pending")

    def test_file_upload(self):
        file_contents = b"Test file contents"
        file = SimpleUploadedFile("test_file.txt", file_contents)
        todo = ToDo.objects.create(
            user_name="TestUser",
            task="File Task",
            description="File Description",
            status="Pending",
            file=file,
        )
        self.assertEqual(todo.file.read(), file_contents)

    def test_blank_description(self):
        todo = ToDo.objects.create(user_name="SomeUser", task="Task with Blank Description")
        self.assertEqual(todo.description, None)
            