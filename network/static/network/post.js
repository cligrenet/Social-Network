document.addEventListener('DOMContentLoaded', function () {
	// post_id injected into index page, one-post-container ==> data-post-id="{{ post.id }}"

	document.querySelectorAll('.one-post-container').forEach((element) => {
		const postId = parseInt(element.dataset.postId);
		const editBtn = element.querySelector('.edit-post-btn');
		const deleteBtn = element.querySelector('.delete-post-btn');
		const likeBtn = element.querySelector('.like-post');

		// Not every post has edit or delete button
		if (editBtn) {
			editBtn.addEventListener('click', () => showTextarea(postId));
		}
		if (deleteBtn) {
			deleteBtn.addEventListener('click', (event) => {
				event.target.closest(
					'.one-post-container'
				).style.animationPlayState = 'running';
				setTimeout(() => {
					deletePost(postId);
				}, 1000);
			});
		}
		if (likeBtn) {
			likeBtn.addEventListener('click', () => toggleLikePost(postId));
		}
	});

	// In utils.js
	renderTimestamps()
});


function showTextarea(postId) {
	// Multiple postWrapper on the same page, use postWrapper.querySelector instead of document.querySelector
	const postWrapper = document.querySelector(
		`.one-post-container[data-post-id='${postId}']`
	);

	postWrapper.querySelector('form').style.display = 'block';
	postWrapper.querySelector('.post-content').style.display = 'none';
	postWrapper.querySelector('.edit-post-btn').style.display = 'none';

	// Ajax, in template better change form into div, no need to preventDefault then
	postWrapper.querySelector('form').addEventListener('submit', (event) => {
		event.preventDefault();
	});
	
	postWrapper
		.querySelector('form .save-post-btn')
		.addEventListener('click', () => savePostEdit(postId));
}


function savePostEdit(postId) {
	const postWrapper = document.querySelector(
		`.one-post-container[data-post-id='${postId}']`
	);
	const csrfToken = postWrapper.querySelector(
		"form [name='csrfmiddlewaretoken']"
	).value;
	const data = postWrapper.querySelector('form textarea').value;

	fetch(`/posts/${postId}`, {
		method: 'PUT',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrfToken,
		},
		body: JSON.stringify({ content: data }),
	})
		.then((response) => {
			if (response.ok) {
				postWrapper.querySelector('.post-content').innerHTML = data;
				// Format post edit date time
				let options = {year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute:'numeric'};
				postWrapper.querySelector(".one-post-timestamp").innerHTML = new Intl.DateTimeFormat('en-US', options).format(new Date());
				postWrapper.querySelector('form').style.display = 'none';
				postWrapper.querySelector('.edit-post-btn').style.display =
					'block';
				postWrapper.querySelector('.post-content').style.display =
					'block';
			}
		})
		.catch((error) => {
			console.error('Error: ', error);
		});
}

function deletePost(postId) {
	const postWrapper = document.querySelector(
		`.one-post-container[data-post-id='${postId}']`
	);
	const csrfToken = postWrapper.querySelector(
		"form [name='csrfmiddlewaretoken']"
	).value;

	fetch(`/posts/${postId}`, {
		method: 'DELETE',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrfToken,
		},
	})
		.then((response) => {
			if (response.ok) {
				postWrapper.remove();
			}
		})
		.catch((error) => {
			console.log('Error: ', error);
		});
}


function toggleLikePost(postId) {
	const postWrapper = document.querySelector(
		`.one-post-container[data-post-id='${postId}']`
	);
	const csrfToken = postWrapper.querySelector(
		"form [name='csrfmiddlewaretoken']"
	).value;

	fetch(`/posts/${postId}/toggle_like`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrfToken,
		},
		body: JSON.stringify({
			post: postId,
		}),
	})
		// response returns a promise, need to wait, then do things with data
		.then((response) => {
			if (response.ok) {
				return response.json();
			} else {
				throw new Error('Failed to toggle like on post.');
			}
		})
		.then((data) => {
			postWrapper.querySelector('.like-count').innerHTML = data.count;
			if (data.liked) {
				postWrapper.querySelector('.like-post').classList.add('liked');
			} else {
				postWrapper
					.querySelector('.like-post')
					.classList.remove('liked');
			}
		})
		.catch((error) => {
			console.log('Error: ', error);
		});
}
