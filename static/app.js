function addPost() {
    const title = document.getElementById('title').value;
    const content = document.getElementById('content').value;

    if (title && content) {
        fetch('/add_post', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ title, content })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            document.getElementById('title').value = '';
            document.getElementById('content').value = '';
            window.location.reload(); // Recarrega a página para exibir o novo post
        })
        .catch(error => console.error('Error:', error));
    }
}

function deletePost(id) {
    fetch(`/delete_post/${id}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
        const postElement = document.getElementById(`post-${id}`);
        if (postElement) {
            postElement.remove();
        }
    })
    .catch(error => console.error('Error:', error));
}

function enableEdit(id) {
    const postElement = document.getElementById(`post-${id}`);
    const titleElement = postElement.querySelector('h2');
    const contentElement = postElement.querySelector('p');
    const editButton = postElement.querySelector('button:nth-of-type(1)');
    const saveButton = postElement.querySelector('button:nth-of-type(2)');

    titleElement.contentEditable = true;
    contentElement.contentEditable = true;
    titleElement.focus();

    editButton.style.display = 'none';
    saveButton.style.display = 'inline';
}

function saveEdit(id) {
    const postElement = document.getElementById(`post-${id}`);
    const titleElement = postElement.querySelector('h2');
    const contentElement = postElement.querySelector('p');
    const editButton = postElement.querySelector('button:nth-of-type(1)');
    const saveButton = postElement.querySelector('button:nth-of-type(2)');

    const title = titleElement.innerText;
    const content = contentElement.innerText;

    if (title && content) {
        fetch(`/edit_post/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ title, content })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            titleElement.contentEditable = false;
            contentElement.contentEditable = false;

            editButton.style.display = 'inline';
            saveButton.style.display = 'none';
        })
        .catch(error => console.error('Error:', error));
    }
}

function addComment(postId) {
    const text = document.getElementById('comment-' + postId).value;
    if (text) {
        fetch('/add_comment/' + postId, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text }),
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            document.getElementById('comment-' + postId).value = '';
            const commentsList = document.getElementById('comments-' + postId);
            const li = document.createElement('li');
            li.id = `comment-${data.comment_id}`;
            li.innerHTML = `${text} - Por: ${data.username}`;

            if (data.is_admin) {
                const deleteButton = document.createElement('button');
                deleteButton.textContent = 'Deletar';
                deleteButton.onclick = function() {
                    deleteComment(data.comment_id);
                };
                li.appendChild(deleteButton);

            }
            
            commentsList.appendChild(li);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }
}

function deleteComment(commentId) {
    fetch(`/delete_comment/${commentId}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
        const commentElement = document.getElementById(`comment-${commentId}`);
        if (commentElement) {
            commentElement.remove();
        }
    })
    .catch(error => console.error('Error:', error));
}

