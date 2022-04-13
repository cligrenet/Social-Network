// Replace template timestamp by javascript, 
// In template one-post and profile, insert data-timestamp to track each post's timestamp (link server-side and client-side timestamp data)
function renderTimestamps() {
	document.querySelectorAll(".one-post-timestamp").forEach((element) => {
		const timestamp = parseInt(element.dataset.timestamp) * 1000
		let options = {year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute:'numeric'}
		element.innerHTML = new Intl.DateTimeFormat('en-US', options).format(new Date(timestamp))
	})
}
