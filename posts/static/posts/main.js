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

//fetching the users from the suggested-users(route)
fetch('/suggested-users/')
  .then(response => response.json())
  .then(data => {
    const suggestedUsersDiv = document.getElementById('suggested-users');

    // Loopin through the users and creating HTML elements for each user
    data.users.forEach(user => {
      const userDiv = document.createElement('div');
      const profileImage = user.profile_image_url || '/path/to/default/image/'; // Replace '/path/to/default/image/' with the default image URL

      userDiv.innerHTML = `
        <a href="/profile/${user.id}">
          <img src="${profileImage}" alt="${user.username}" width="50" height="50">
          <span>${user.username}</span>
        </a>
        <a href="/follow-user/${user.id}" class="btn btn-primary btn-sm">Follow</a>
      `;

      suggestedUsersDiv.appendChild(userDiv);
    });
  })
  .catch(error => {
    console.error('Error fetching suggested users:', error);
  });