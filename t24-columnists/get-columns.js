unction checkForNewElements() {
  var numElements = document.querySelectorAll('._2Mepd ._1fE_V').length;
  window.scrollTo(0, document.body.scrollHeight);
  setTimeout(function() {
    var newNumElements = document.querySelectorAll('._2Mepd ._1fE_V').length;
    if (newNumElements > numElements) {
      // More elements have been added, continue scrolling
      checkForNewElements();
    } else {
      var moreButton = document.querySelector('#MoreButton');
      if (moreButton) {
        var moreButtonRect = moreButton.getBoundingClientRect();
        if (moreButtonRect.top < window.innerHeight) {
          // #MoreButton element is in the viewport, scroll to the top of the page
          window.scrollTo(0, 0);
          // Wait for scrolling to complete before scrolling down again
          setTimeout(function() {
            // Scroll down to the bottom of the page again
            window.scrollTo(0, document.body.scrollHeight);
            // Wait for scrolling to complete before checking for new elements
            setTimeout(function() {
              // Get all elements with class '_2Mepd' and '_1fE_V'
              var elements = document.querySelectorAll('._2Mepd ._1fE_V');
              var results = [];
              for (var i = 0; i < elements.length; i++) {
                var element = elements[i];
                // Get the 'h3' element inside the '_31Tbh' element and extract the text content
                var h3 = element.querySelector('._31Tbh h3');
                var h3Text = h3 ? h3.textContent : '';
                // Get the 'a' element inside the '_31Tbh' element and extract the 'href' attribute
                var a = element.querySelector('._31Tbh a');
                var href = a ? a.getAttribute('href') : '';
                // Get the 'p' element inside the '_31Tbh' element and extract the text content
                var p = element.querySelector('._31Tbh p');
                var pText = p ? p.textContent : '';
                // Get the second 'p' element inside the '_2J9OF' element and extract the text content
                var secondP = element.querySelector('._2J9OF p:nth-of-type(2)');
                var secondPText = secondP ? secondP.textContent : '';
                // Add the extracted information to an object and push it to the 'results' array
                var result = {
                  title: h3Text,
                  path: 'https://t24.com.tr' + href,
                  description: pText,
                  date: secondPText
                };
                results.push(result);
              }
              console.log('Results:', results);
              // Call the function recursively to check for new elements
              checkForNewElements();
            }, 2000);
          }, 2000);
        } else {
          // #MoreButton element is not in the viewport, wait and check for new elements
          setTimeout(checkForNewElements, 2000);
        }
      } else {
        // #MoreButton element not found, stop executing
        console.log('No more elements being added.');
      }
    }
  }, 2000);
}

checkForNewElements();
