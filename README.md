# Django Blog Project

## Overview
This is a simple Django-based blog application that allows users to register, log in, and interact with posts. The blog supports user authentication, post creation, tagging, and commenting.

## Features
- **User Authentication**: Registration, login, and logout functionality.
- **Posts**: Displaying all posts and viewing individual post details.
- **Tags**: Categorization of posts using tags.
- **Comments**: Users can comment on posts.

## Installation
### Prerequisites
Ensure you have Python and Django installed.

```bash
python -m venv venv
source venv/bin/activate  # On Windows use 'venv\\Scripts\\activate'
pip install -r requirements.txt
```

## Usage
### Running the Server
To start the Django development server, run:

```bash
python manage.py runserver
```

Access the application at `http://127.0.0.1:8000/`.

## Models
### 1. **Tag**
```python
class Tag(models.Model):
    caption = models.CharField(max_length=50)
```
Used to categorize posts.

### 2. **Author**
```python
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email_address = models.EmailField(unique=True)
```
Holds author details.

### 3. **Post**
```python
class Post(models.Model):
    title = models.CharField(max_length=200)
    excerpt = models.CharField(max_length=300)
    image = models.ImageField(upload_to="posts", null=True)
    date = models.DateField(auto_now=True)
    slug = models.SlugField(unique=True, db_index=True)
    content = models.TextField(validators=[MinLengthValidator(10)])
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name="posts")
    tags = models.ManyToManyField(Tag)
```
Handles blog posts.

### 4. **Comment**
```python
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, related_name="comments")
    comment_text = models.TextField()
```
Stores comments for posts.

## Views
### 1. **Register**
Handles user registration.
```python
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'blog/register.html')
        user = User.objects.create_user(username=username, password=password)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('login')
    return render(request, 'blog/register.html')
```

### 2. **Logout**
```python
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')
```

### 3. **View Posts**
```python
@login_required
def posts(request):
    all_posts = Post.objects.all()
    return render(request, "blog/all-post.html", {"all_posts": all_posts})
```

### 4. **View Post Details and Commenting**
```python
@login_required
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post-detail-page', slug=slug)
    else:
        form = CommentForm()
    return render(request, "blog/post-detail.html", {"post": post, "form": form})
```

## License
This project is licensed under the MIT License.

---
Feel free to contribute or modify as needed!

