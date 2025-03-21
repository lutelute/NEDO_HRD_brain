const clickToEnlarge = "Click and hold to enlarge. SHIFT + wheel to zoom. ESC to reset.";
const clickToCollapse = "ESC to reset. Click and hold to collapse. SHIFT + wheel to zoom";

// Check if in iFrame - if yes the page is assumed to be an embedded frame
if (window.self !== window.top) {
  ["div.site-body-right-column", "div.site-body-left-column", "div.site-header", "div.site-footer"].forEach(selector => {
    document.querySelectorAll(selector).forEach(div => {
      div.style.display = "none";
    });
  });
}

const correctUrlEncoding = (url) => {
  try {
    return decodeURIComponent(escape(url));
  } catch (e) {
    return decodeURIComponent(url);
  }
};

const addNavigationToDiv = (container) => {
  const svgElement = container?.querySelector('svg');
  if (!svgElement) return;

  container.classList.add("excalidraw-svg");
  svgElement.removeAttribute("width");
  svgElement.removeAttribute("height");

  const textDiv = document.createElement('div');
  textDiv.className = 'text';
  textDiv.textContent = clickToEnlarge;
  container.appendChild(textDiv);

  let isEnlarged = false;
  let zoomLevel = 1;
  let panX = 0;
  let panY = 0;
  let isPanning = false;
  let panStartX = 0;
  let panStartY = 0;
  let timeout = null;

  const applyTransform = () => {
    svgElement.style.transform = `scale(${zoomLevel}) translate(${panX}px, ${panY}px)`;
  };

  // Zoom with Shift + Mouse Wheel
  svgElement.addEventListener('wheel', (event) => {
    if (!event.shiftKey) return;
    zoomLevel += event.deltaY > 0 ? -0.1 : 0.1;
    zoomLevel = Math.max(0.5, Math.min(zoomLevel, 10));
    applyTransform();
  });

  // Panning with Mouse Drag
  svgElement.addEventListener('mousedown', (event) => {
    isPanning = true;
    panStartX = event.clientX;
    panStartY = event.clientY;
  });

  svgElement.addEventListener('mousemove', (event) => {
    if (!isPanning) return;
    panX += (event.clientX - panStartX) / zoomLevel;
    panY += (event.clientY - panStartY) / zoomLevel;
    panStartX = event.clientX;
    panStartY = event.clientY;
    applyTransform();
  });

  svgElement.addEventListener('mouseup', () => isPanning = false);
  svgElement.addEventListener('mouseleave', () => isPanning = false);

  // Reset with ESC key
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      isEnlarged = false;
      zoomLevel = 1;
      panX = 0;
      panY = 0;
      container.classList.remove("enlarged");
      textDiv.textContent = clickToEnlarge;
      applyTransform();
    }
  });

  // Toggle enlarge on long press
  svgElement.addEventListener('mousedown', () => {
    timeout = setTimeout(() => {
      if (isEnlarged) {
        container.classList.remove("enlarged");
        textDiv.textContent = clickToEnlarge;
      } else {
        container.classList.add("enlarged");
        textDiv.textContent = clickToCollapse;
      }
      isEnlarged = !isEnlarged;
    }, 1000);
  });

  svgElement.addEventListener('mouseup', () => clearTimeout(timeout));
  applyTransform();
};

const processIMG = (img) => {
  const svgURL = img.src;
  const container = img.parentElement;

  fetch(svgURL)
    .then(response => response.ok ? response.text() : Promise.reject('Failed to fetch SVG'))
    .then(svgContent => {
      const svgContainer = document.createElement('div');
      svgContainer.innerHTML = svgContent;

      svgContainer.querySelectorAll(`a[href]`).forEach(el => {
        let href = el.getAttribute("href");
        if (href.startsWith("obsidian://open?vault=")) {
          let filePart = href.split('&file=')[1] || "";
          let webUrl = "https://www.nedo-hrd.online/" + decodeURIComponent(filePart);
          el.setAttribute("href", webUrl);
        }
      });

      svgContainer.querySelectorAll(`iframe[src]`).forEach(el => {
        let src = el.getAttribute("src");
        if (src.startsWith("obsidian://open?vault=")) {
          let filePart = src.split('&file=')[1] || "";
          let webUrl = "https://www.nedo-hrd.online/" + decodeURIComponent(filePart);
          el.setAttribute("src", webUrl);
        }
      });

      container.removeChild(img);
      container.appendChild(svgContainer);
      addNavigationToDiv(svgContainer);
    })
    .catch(error => console.error('Error:', error));
};

const addImgMutationObserver = () => {
  const observer = new MutationObserver(mutationsList => {
    for (const mutation of mutationsList) {
      if (mutation.type === 'childList') {
        mutation.addedNodes.forEach(node => {
          if (node instanceof Element && node.querySelector(`img[alt$=".svg"]`)) {
            processIMG(node.querySelector(`img[alt$=".svg"]`));
          }
        });
      }
    }
  });

  observer.observe(document.body, { childList: true, subtree: true });
};

// Process images after loading
document.body.querySelectorAll(`img[alt$=".svg"]`).forEach(processIMG);
addImgMutationObserver();