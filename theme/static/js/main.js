document.addEventListener('DOMContentLoaded', () => {
    const lazyVideos = document.querySelectorAll('.yt-lazy-wrapper');

    lazyVideos.forEach(wrapper => {
        wrapper.addEventListener('click', () => {
            const videoId = wrapper.dataset.videoId;
            const title = wrapper.dataset.title;

            // Vytvoříme iframe
            const iframe = document.createElement('iframe');
            iframe.setAttribute('width', '100%');
            iframe.setAttribute('height', '450');
            iframe.setAttribute('src', `https://www.youtube-nocookie.com/embed/${videoId}?autoplay=1`);
            iframe.setAttribute('title', title);
            iframe.setAttribute('frameborder', '0');
            iframe.setAttribute('allow', 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture');
            iframe.setAttribute('referrerpolicy', 'strict-origin-when-cross-origin');
            iframe.setAttribute('allowfullscreen', '');

            // Nahradíme náhled iframe
            wrapper.replaceWith(iframe);
        });
    });
});
