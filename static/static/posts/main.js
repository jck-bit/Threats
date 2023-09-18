document.querySelectorAll('.like-link').forEach(link => {
    link.addEventListener('click', function (event) {
        event.preventDefault();
        const postId = link.dataset.postId;
        fetch(`/like-post?post_id=${postId}`)
            .then(response => response.json())
            .then(data => {

                link.querySelector('span').textContent = data.likes_count;
                if (data.liked) {
                    link.classList.add('liked');
                } else {
                    link.classList.remove('liked');
                }
            })
            .catch(error => console.error('Error:', error));
    });
});

