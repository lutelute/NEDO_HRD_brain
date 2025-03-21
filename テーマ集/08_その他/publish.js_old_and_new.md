

```js
const clickToEnlarge = "Click and hold to enlarge. SHIFT + wheel to zoom. ESC to reset.";
const clickToCollapse = "ESC to reset. Click and hold to collapse. SHIFT + wheel to zoom";

//check if in iFrame - if yes the page is assumed to be an embedded frame
if(window.self !== window.top) {
  const elements = [
    "div.site-body-right-column",
    "div.site-body-left-column",
    "div.site-header",
    "div.site-footer"
  ];
  elements.forEach(x=>{
    document.querySelectorAll(x).forEach(div=>{
      div.style.display = "none";
    });
  });
}

const baseUrl = `${window.location.origin}/`;

const [isDesktop, isMobile, isTablet] = (()=>{
  const userAgent = navigator.userAgent;
  const mobileKeywords = ['Mobile', 'Android', 'iPhone', 'iPad', 'Windows Phone'];

  const isMobile = mobileKeywords.some(keyword => userAgent.includes(keyword));
  const isTablet = /iPad/i.test(userAgent) || (isMobile && !/Mobile/i.test(userAgent));
  const isDesktop = !isMobile && !isTablet;

  return [isDesktop, isMobile, isTablet];
})();

const addNavigationToDiv = (container) => {
  const svgElement = container?.querySelector('.excalidraw-svg');
  if(!svgElement) return;
  container.addClass("excalidraw-svg");
  svgElement.removeAttribute("width");
  svgElement.removeAttribute("height");
  
  if(!isDesktop) return;
  
  const textDiv = document.createElement('div');
  textDiv.className = 'text';
  textDiv.textContent = clickToEnlarge;
  container.appendChild(textDiv);

  let isEnlarged = false;
  let timeout = null;
  let isReadyToPan = false;
  let isPanning = false;
  let zoomLevel = 1;
  let panX = 0;
  let panY = 0;
  let pinchStartDistance = 0;
  let panStartX = 0;
  let panStartY = 0;

  const clearEnlargeTimeout = () => {
    if(timeout) clearTimeout(timeout);
    timeout = null;
  }

  const enablePointerEvents = (val) => {
    svgElement.querySelectorAll("a").forEach(el=>{
      el.style.pointerEvents = val ? "all" : "none";
    });
  }

  const applyTransform = () => {
    svgElement.style.transform = `scale(${zoomLevel}) translate(${panX}px, ${panY}px)`;
    clearEnlargeTimeout();
  };

  //Wheel zoom
  svgElement.addEventListener('wheel', (event) => {
    if(!event.shiftKey ) return;
    if (event.deltaY > 0) {
    zoomLevel -= zoomLevel > 4 
	  ? (zoomLevel > 6 
	    ? (zoomLevel > 10 ? 0.4 : 0.3)
		: 0.2) 
	  : 0.1;
    } else {
    zoomLevel += zoomLevel > 4 
	  ? (zoomLevel > 6 
	    ? (zoomLevel > 10 ? 0.4 : 0.3)
		: 0.2) 
	  : 0.1;
    }
    applyTransform();
  });

  // Panning
  svgElement.addEventListener('mousedown', (event) => {
    isReadyToPan = true;
    panStartX = event.clientX;
    panStartY = event.clientY;
  });

  svgElement.addEventListener('mousemove', (event) => {
    const deltaX = event.clientX - panStartX;
    const deltaY = event.clientY - panStartY;
    const distance = Math.sqrt(deltaX**2+deltaY**2);
    if (isReadyToPan && (distance > 20)) {
      if(!isPanning) {
        enablePointerEvents(false);
        isPanning = true;
      }
      panX += deltaX/zoomLevel;
      panY += deltaY/zoomLevel;
      panStartX = event.clientX;
      panStartY = event.clientY;

      applyTransform();
    }
  });

  svgElement.addEventListener('mouseup', () => {
    enablePointerEvents(true);
    isPanning = false;
    isReadyToPan = false;
  });

  svgElement.addEventListener('mouseleave', () => {
    enablePointerEvents(true);
    isPanning = false;
    isReadyToPan = false;
  });

  //abort on Escape
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      enablePointerEvents(true);
      isEnlarged = false;
      isPanning = false;
      isReadyToPan = false;
      container.classList.remove("enlarged");
      textDiv.textContent = clickToEnlarge;
      zoomLevel = 1;
      panX = 0;
      panY = 0;
      applyTransform();
    }
  });
 

  //Enlarge on long click
  svgElement.addEventListener('mouseup', () => clearEnlargeTimeout());
  svgElement.addEventListener('mousedown', () => {
    timeout = setTimeout(()=> {
      timeout = null;
      if(isPanning) return;
      isReadyToPan = false;
      if (isEnlarged) {
        // Collapse the image
        container.classList.remove("enlarged");
        textDiv.textContent = clickToEnlarge;
      } else {
        // Enlarge the image
        container.addClass("enlarged");
        textDiv.textContent = clickToCollapse;
      }
      isEnlarged = !isEnlarged;
    },1000);
  });

  applyTransform();
}

const processIMG = (img) => {
  const svgURL = img.src;
  const container = img.parentElement;

  fetch(svgURL)
    .then((response) => {
      if (response.ok) {
        return response.text();
      }
      throw new Error('Failed to fetch SVG');
    })
    .then((svgContent) => {    
      svgContainer = document.createElement('div');
      svgContainer.innerHTML = svgContent;
      svgContainer.querySelectorAll(`a[href^="obsidian://open?vault="`).forEach(el=>{
        el.setAttribute("href",unescape(el.getAttribute("href").replace(/.*&file=/,baseUrl).replaceAll(" ","+")));
      });
      svgContainer.querySelectorAll(`iframe[src^="obsidian://open?vault="`).forEach(el=>{
        el.setAttribute("src",unescape(el.getAttribute("src").replace(/.*&file=/,baseUrl).replaceAll(" ","+")));
      });
      container.removeChild(img);
      container.appendChild(svgContainer);
      addNavigationToDiv(svgContainer);
      
    })
    .catch((error) => {
      console.error('Error: ' + error);
    });
}

const addImgMutationObserver = () => {
  const targetElement = document.body;
  const handleImgAddition = (mutationsList, observer) => {
    for (const mutation of mutationsList) {
      if (mutation.type === 'childList') {
    mutation.addedNodes.forEach(node => {
      if (node instanceof Element && node.querySelector(`img[alt$=".svg"]`)) {
        processIMG(node.querySelector(`img[alt$=".svg"]`));
      };
        });
      }
    }
  }
  const observer = new MutationObserver(handleImgAddition);
  const config = { childList: true, subtree: true };
  observer.observe(targetElement, config);
}

//process images after loading
document.body.querySelectorAll(`img[alt$=".svg"`).forEach(img => {
  processIMG(img);
});

addImgMutationObserver();
```


```js
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

```