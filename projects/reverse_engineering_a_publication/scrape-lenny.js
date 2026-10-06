(function () {
    const articles = document.querySelectorAll('[role="article"]');
    let data = 'Title\tLink\tDescription\tPublished\tAuthor\tHearts\tComments\n'; // Header row

    data += Array.from(articles).map(container => {
        try {
            const links = container.querySelectorAll('a');
            const titleLink = links[0];
            const descriptionLink = links[1];
            const authorLinks = Array.from(links).slice(2);

            const title = titleLink ? titleLink.textContent.trim() : '';
            const link = titleLink ? titleLink.href : '';
            const description = descriptionLink ? descriptionLink.textContent.trim() : '';

            const timeElement = container.querySelector('time');
            const published = timeElement ? timeElement.textContent.trim() : '';

            const author = authorLinks.map(a => a.textContent.trim()).join(', ');

            const likeButton = container.querySelector('button[aria-label^="Like"]');
            const commentButton = container.querySelector('button[aria-label^="View comments"]');
            const hearts = likeButton ? likeButton.textContent.trim() : '0';
            const comments = commentButton ? commentButton.textContent.trim() : '0';

            return `"${title}"\t"${link}"\t"${description}"\t"${published}"\t"${author}"\t${hearts}\t${comments}`;

        } catch (err) {
            console.error('Error parsing article:', err);
            return '\t\t\t\t\t\t';
        }

    }).join('\n');

    const textArea = document.createElement('textarea');
    textArea.value = data;
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    try {
        document.execCommand('copy');
        console.log('Data copied to clipboard! You can paste it into your Google Sheets.');
    } catch (err) {
        console.error('Failed to copy, please manually select and copy.');
    }
    document.body.removeChild(textArea);
})();