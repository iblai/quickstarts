// Update the following variables to match the environment we want to use.

// The mentor origin
const MENTOR_ORIGIN = 'https://mentor.example.com'

// The tenant or platform to use
const PLATFORM = 'main'

// The slug of the mentor to chat with
const MENTOR_SLUG = 'ai-mentor'

// Logo icon to use
const ICON_IMAGE_URL = 'https://example.com/image/image.png'



window.onload = () => {
    let iframeContainer = document.createElement('div');
    iframeContainer.id = 'ibl-chat-widget-container';
    iframeContainer.style = "position: fixed; border-radius: 13px; bottom: 96px; right: 60px; z-index: 2147483647; width: 400px; height: 82%;box-shadow:0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)";
    let bubble = document.createElement('img');
    bubble.src = ICON_IMAGE_URL;
    bubble.style = "position: fixed; right: 60px; bottom: 20px; height: 50px;cursor:pointer;";
    bubble.addEventListener('click', () => {
        const widget = document.getElementById('ibl-chat-widget-container');
        if(widget.style.display === 'none'){
            widget.style.display = '';
        }else{
            widget.style.display = 'none';
        }
    });
    let iframe = document.createElement('iframe');
    iframe.src = `${MENTOR_ORIGIN}/platform/${PLATFORM}/${MENTOR_SLUG}?embed=true&mode=anonymous&extra-body-classes=iframed-externally`;
    iframe.style = "border: 0px white; height:100%;width:100%;border-radius: 13px;";
    iframe.allow = "clipboard-read; clipboard-write"

    iframeContainer.appendChild(iframe);
    document.body.appendChild(iframeContainer);
    document.body.appendChild(bubble);
}

