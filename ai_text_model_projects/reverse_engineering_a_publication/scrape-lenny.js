(function () {
    const articles = document.querySelectorAll('.pencraft.pc-display-flex.pc-flexDirection-column.pc-padding-8.pc-reset.pc-borderRadius-sm._container_1uybr_1');
    let data = 'Title\tLink\tDescription\tPublished\tAuthor\tHearts\tComments\n'; // Header row

    data += Array.from(articles).map(container => {
        try {
            const article = container.querySelector('.pencraft.pc-display-flex.pc-flexDirection-column.pc-gap-8.pc-position-relative.pc-reset')

            const titleElement = article.children[0] || { innerText: '', href: '' };
            const descriptionElement = article.children[1] || { innerText: '' };
            const heartsElement = container.querySelector('.like-button-container .label');
            const commentsElement = container.querySelector('.post-ufi-comment-button .label');
            const publishedElement = article.children[2];

            const title = titleElement.innerText.trim();
            const link = titleElement.firstChild.href;
            const description = descriptionElement.innerText.trim();
            const hearts = heartsElement ? heartsElement.innerText.trim() : '0';
            const comments = commentsElement ? commentsElement.innerText.trim() : '0';
            const published = publishedElement ? publishedElement.children[0].innerText.trim() : '';
            const author = publishedElement ? publishedElement.children[2].innerText.trim() : '';

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