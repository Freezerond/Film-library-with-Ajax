document.addEventListener('DOMContentLoaded', () => {
  const commentForm = document.getElementById('comment-form');
  const commentsContainer = document.getElementById('comments-container');

  if (commentForm) {
    commentForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      if (!document.body.dataset.auth || document.body.dataset.auth === 'false') {
        window.location.href = '/login';
        return;
      }

      const formData = new FormData(commentForm);
      const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

      const response = await fetch(window.location.href, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken,
          'X-Requested-With': 'XMLHttpRequest'
        },
        body: formData
      });

      if (response.ok) {
        const data = await response.json();
        const placeholder = document.getElementById('no-comments');
        if (placeholder) {
          placeholder.remove();
        }
        commentsContainer.insertAdjacentHTML('afterbegin', data.comment_html);
        commentForm.reset();
      }
    });
  }

  commentsContainer.addEventListener('click', async (e) => {
    if (e.target.classList.contains('delete-comment')) {
      const commentId = e.target.dataset.id;

      const response = await fetch(`/delete_comment/${commentId}/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value }
      });

      if (response.ok) {
        document.getElementById(`comment-${commentId}`).remove();

        if (commentsContainer.querySelectorAll('[id^="comment-"]').length === 0) {
        const noComments = document.createElement('p');
        noComments.id = 'no-comments';
        noComments.textContent = 'Комментариев пока нет.';
        commentsContainer.appendChild(noComments);
        }
      }
    }
  });

  const vote = async (value) => {
  const isAuthenticated = document.body.dataset.auth === 'true';
  if (!isAuthenticated) {
    window.location.href = '/login';  // или {% url 'login' %}, если генерируешь ссылку в шаблоне
    return;
  }

  const response = await fetch('/vote/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
    },
    body: JSON.stringify({
      movie_id: document.querySelector('body').dataset.movieId,
      vote: value
    })
  });

    if (response.ok) {
      const data = await response.json();
      document.getElementById('like-count').textContent = data.likes;
      document.getElementById('dislike-count').textContent = data.dislikes;
    }
  };

  document.getElementById('like-button')?.addEventListener('click', () => vote(1));
  document.getElementById('dislike-button')?.addEventListener('click', () => vote(-1));
});
