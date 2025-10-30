function html_printer(...selectors) {
  if (!selectors.length) {
    alert("Please provide at least one selector.");
    return;
  }

  // Collect matching elements from all selectors
  const elements = selectors.flatMap((sel) =>
    Array.from(document.querySelectorAll(sel))
  );
  if (!elements.length) {
    alert("No elements found for: " + selectors.join(", "));
    return;
  }

  // Deep clone each element and apply computed styles
  const clones = elements.map((elem) => {
    const clone = elem.cloneNode(true);

    const applyComputedStyles = (src, dest) => {
      const computed = window.getComputedStyle(src);
      for (const prop of computed) {
        dest.style[prop] = computed.getPropertyValue(prop);
      }
    };

    applyComputedStyles(elem, clone);
    const srcChildren = elem.getElementsByTagName("*");
    const destChildren = clone.getElementsByTagName("*");
    for (let i = 0; i < srcChildren.length; i++) {
      applyComputedStyles(srcChildren[i], destChildren[i]);
    }

    return clone;
  });

  // Collect all style, font, and script resources for proper rendering
  const headNodes = Array.from(
    document.querySelectorAll(
      'link[rel="stylesheet"], style, link[rel="preconnect"], link[rel*="font"], script'
    )
  );

  // Open a new window for printing
  const printWindow = window.open("", "", "width=900,height=700");
  if (!printWindow) {
    alert("Pop-up blocked! Please allow pop-ups for this site.");
    return;
  }

  const doc = printWindow.document;
  const html = doc.documentElement;
  const head = doc.createElement("head");
  const body = doc.createElement("body");

  // Clone head resources
  headNodes.forEach((node) => head.appendChild(node.cloneNode(true)));

  // Add basic print-friendly styling
  const style = doc.createElement("style");
  style.textContent = `
    body {
      margin: 20px;
      font-family: inherit;
    }
    hr {
      margin: 40px 0;
      border: 1px dashed #ccc;
    }
  `;
  head.appendChild(style);

  // Add cloned elements with divider lines
  clones.forEach((clone, i) => {
    body.appendChild(clone);
    if (i < clones.length - 1) {
      const hr = doc.createElement("hr");
      body.appendChild(hr);
    }
  });

  // Assemble full document
  html.appendChild(head);
  html.appendChild(body);
  doc.replaceChildren(html);

  // Wait until ready, then print
  printWindow.onload = () => {
    printWindow.focus();
    printWindow.print();
  };
}

// If script is loaded show a success message in the console as well as an alert
console.log(
  "%cfile 'html_printer.js' loaded successfully, use the function 'html_printer(selector1, selector2, ...)' to print specific elements.",
  "color: green; font-weight: bold;"
);
alert(
  "file 'html_printer.js' loaded successfully, use the function 'html_printer(selector1, selector2, ...)' to print specific elements."
);
