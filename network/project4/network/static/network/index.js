document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.edit-button').forEach(button => {
        button.addEventListener('click', function editHandler() {
            const post_id = this.getAttribute('data-post_id');
            const post_text = document.getElementById(`post-text-${post_id}`);
            const textarea = document.getElementById(`textarea-${post_id}`);

            textarea.style.display = "block";
            textarea.value = post_text.innerHTML; 

            this.textContent = 'Save';

            this.removeEventListener('click', editHandler); 
            this.addEventListener('click', function saveHandler() {
                post_text.innerHTML = textarea.value; 
                textarea.style.display = "none";

                fetch(`/edit_post/${post_id}`, {
                    method: 'PUT',
                    body: JSON.stringify({ text: textarea.value })
                  })

                  .then(response => {
                        this.textContent = 'Edit';
                        this.classList.remove('save-button');
                        this.classList.add('edit-button');

                        this.removeEventListener('click', saveHandler); 
                        this.addEventListener('click', editHandler); 
                })
                .catch(error => console.error('Erro:', error));
            });
        });
    });

    
    document.querySelectorAll(".like-container").forEach(like => {
        like.addEventListener("click", function likeHandler() {
            const post_id = this.getAttribute('data-post_id');
            let liked = this.getAttribute('data-liked'); 
            let likesCount = parseInt(this.getAttribute('data-likes'));
    
            if (liked === 'true') {
                fetch(`/unlike/${post_id}`, {
                    method: 'POST',
                })
                .then(response => response.json())
                .then(result => {
                    console.log(result.status);
                    const button = this.querySelector('button');
                    button.classList.remove('btn-dislike');
                    button.classList.add('btn-like');
                    button.innerHTML = '<i class="bi bi-hand-thumbs-up-fill"></i>';
                    this.setAttribute('data-liked', 'false'); 
                    
                    const countElement = document.getElementById(`like-count-${post_id}`);
                    countElement.textContent = parseInt(countElement.textContent) - 1;

                    
                })
                .catch(error => console.error('Error unliking:', error));
            } else {
                fetch(`/like/${post_id}`, {
                    method: 'POST',
                })
                .then(response => response.json())
                .then(result => {
                    console.log(result.status);
                    const button = this.querySelector('button');
                    button.classList.remove('btn-like');
                    button.classList.add('btn-dislike');
                    button.innerHTML = '<i class="bi bi-hand-thumbs-down-fill"></i>';
                    this.setAttribute('data-liked', 'true'); 

                    const countElement = document.getElementById(`like-count-${post_id}`);
                    countElement.textContent = parseInt(countElement.textContent) + 1;

                })
                .catch(error => console.error('Error liking:', error));
            }
        });
    });
    

});
