document.addEventListener('DOMContentLoaded', () => {
    try { // Add a try...catch block to see any errors
        const filterInputs = document.querySelectorAll('.filter-checkbox, .filter-range-min, .filter-range-max');

        // Read URL parameters and set filters
        function setFiltersFromURL() {
            const params = new URLSearchParams(window.location.search);
            
            console.log('URL params:', Array.from(params.entries())); // Debug log
            
            params.forEach((value, key) => {
                console.log(`Processing param: ${key} = ${value}`); // Debug log
                
                // Convert URL parameter to a normalized search string (lowercase, spaces)
                const searchName = key.replace(/-/g, ' ').toLowerCase();
                console.log(`Looking for filter: ${searchName}`); // Debug log
                
                // Find filter element by matching data-filter attribute (case-insensitive)
                let filterEl = null;
                document.querySelectorAll('[data-filter]').forEach(el => {
                    const filterName = el.dataset.filter.toLowerCase();
                    if (filterName === searchName) {
                        filterEl = el.closest('.filter');
                    }
                });
                
                if (filterEl) {
                    console.log(`Found filter element for: ${searchName}`); // Debug log
                    const filterType = filterEl.querySelector('[data-filter-type]').dataset.filterType;
                    
                    if (filterType === 'multi-select') {
                        // Split multiple values by comma
                        const values = value.split(',');
                        values.forEach(v => {
                            const checkbox = filterEl.querySelector(`input[type="checkbox"][value="${v.trim()}"]`);
                            console.log(`Looking for checkbox with value: ${v.trim()}, found:`, checkbox); // Debug log
                            if (checkbox) {
                                checkbox.checked = true;
                            }
                        });
                    } else if (filterType === 'date-range') {
                        const [min, max] = value.split(',');
                        if (min) filterEl.querySelector('.filter-range-min').value = min;
                        if (max) filterEl.querySelector('.filter-range-max').value = max;
                    }
                } else {
                    console.log(`Filter element NOT found for: ${searchName}`); // Debug log
                }
            });
        }

        function getActiveFilters() {
            const activeFilters = {};
            const filterElements = document.querySelectorAll('.filter');

            filterElements.forEach(filterEl => {
                const filterName = filterEl.querySelector('[data-filter]').dataset.filter;
                const filterType = filterEl.querySelector('[data-filter-type]').dataset.filterType;
                const allCheckboxes = filterEl.querySelectorAll('input[type="checkbox"]');

                if (filterType === 'multi-select') {
                    const checked = filterEl.querySelectorAll('input[type="checkbox"]:checked');
                    // Only apply filter if at least one checkbox is checked
                    if (checked.length > 0) {
                        activeFilters[filterName] = Array.from(checked).map(cb => cb.value);
                    }
                    // If no checkboxes are checked, don't add this filter to activeFilters
                    // (this means "don't filter by this category")
                } else if (filterType === 'date-range') {
                    const minVal = filterEl.querySelector('.filter-range-min').value;
                    const maxVal = filterEl.querySelector('.filter-range-max').value;
                    activeFilters[filterName] = {
                        min: minVal ? parseInt(minVal, 10) : -Infinity,
                        max: maxVal ? parseInt(maxVal, 10) : Infinity
                    };
                }
            });
            return activeFilters;
        }

        function filterProducts() {
            const filters = getActiveFilters();
            const productCards = document.querySelectorAll('.product-card');

            productCards.forEach(card => {
                let isVisible = true;

                for (const filterName in filters) {
                    const filterValue = filters[filterName];
                    const dataAttrName = `data-${filterName.toLowerCase().replace(/\s+/g, '-')}`;
                    const cardAttrValue = card.getAttribute(dataAttrName);

                    if (Array.isArray(filterValue)) { // multi-select
                        if (!cardAttrValue) {
                            isVisible = false;
                            break;
                        }

                        // Split by || for multi-value attributes
                        const cardValues = cardAttrValue.split('||').map(v => v.trim());
                        // Check if ANY card value is included in the selected filters
                        const match = cardValues.some(v => filterValue.includes(v));
                        if (!match) {
                            isVisible = false;
                            break;
                        }
                    } else { // date-range
                        if (!cardAttrValue) {
                            isVisible = false;
                            break;
                        }
                        const cardYear = parseInt(cardAttrValue.split(' - ')[0], 10);
                        if (cardYear < filterValue.min || cardYear > filterValue.max) {
                            isVisible = false;
                            break;
                        }
                    }
                }

                card.style.display = isVisible ? '' : 'none';
            });

            // Update counter after filtering
            updateCounter();
        }

        filterInputs.forEach(input => {
            input.addEventListener('change', filterProducts);
        });

        // Set filters from URL parameters, then filter
        setFiltersFromURL();
        filterProducts();
    } catch (error) {
        console.error("An error occurred during filter initialization:", error);
    }

    // Toggle button for mobile sidebar
    console.log("Setting up sidebar toggle..."); // Check if this part of the script is reached
    const toggleBtn = document.getElementById('toggle-filters-btn');
    const sidebar = document.querySelector('.sidebar');

    console.log("Toggle button:", toggleBtn); // Check if the button was found
    console.log("Sidebar element:", sidebar); // Check if the sidebar was found

    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener('click', function() {
            console.log("Toggle button clicked!"); // Check if the click event fires
            sidebar.classList.toggle('active');
            console.log("Sidebar active class toggled. Current classes:", sidebar.className); // See the result
            
            // Change button text with icon
            if (sidebar.classList.contains('active')) {
                toggleBtn.innerHTML = '<i class="fas fa-times"></i> Hide Filters';
            } else {
                toggleBtn.innerHTML = '<i class="fas fa-filter"></i> Show Filters';
            }
        });
        console.log("Sidebar toggle event listener attached successfully.");
    } else {
        console.error("Could not find the toggle button or the sidebar element.");
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const searchCount = document.getElementById('searchResults');
    
    if (!searchInput) return;
    
    // Get all cards (adjust selector based on your card class)
    const cards = document.querySelectorAll('.product-card');
    
    // Store original HTML for each card
    const originalHTML = new Map();
    cards.forEach(card => {
        originalHTML.set(card, card.innerHTML);
    });
    
    searchInput.addEventListener('input', function(e) {
        const query = normalizeText(e.target.value.toLowerCase().trim());
        
        cards.forEach(card => {
            // Restore original HTML
            card.innerHTML = originalHTML.get(card);
            
            if (query === '') {
                // Show all cards when search is empty
                card.classList.remove('hidden');
            } else {
                // Get all searchable text in the card
                const cardText = normalizeText(card.textContent.toLowerCase());
                
                if (cardText.includes(query)) {
                    card.classList.remove('hidden');
                    highlightText(card, query);
                } else {
                    card.classList.add('hidden');
                }
            }
        });

        // Update the general counter after search
        updateCounter();
    });
    
    function highlightText(element, query) {
        const normalizedQuery = normalizeText(query);
        
        function highlightNode(node) {
            if (node.nodeType === Node.TEXT_NODE) {
                const text = node.nodeValue;
                const normalizedText = normalizeText(text.toLowerCase());
                
                // Find matches in normalized text
                const matches = [];
                let index = normalizedText.indexOf(normalizedQuery);
                while (index !== -1) {
                    matches.push(index);
                    index = normalizedText.indexOf(normalizedQuery, index + 1);
                }
                
                if (matches.length > 0) {
                    const fragments = [];
                    let lastIndex = 0;
                    
                    matches.forEach(matchIndex => {
                        // Add text before match
                        if (matchIndex > lastIndex) {
                            fragments.push({
                                text: text.substring(lastIndex, matchIndex),
                                highlight: false
                            });
                        }
                        
                        // Add matched text (with original accents)
                        fragments.push({
                            text: text.substring(matchIndex, matchIndex + normalizedQuery.length),
                            highlight: true
                        });
                        
                        lastIndex = matchIndex + normalizedQuery.length;
                    });
                    
                    // Add remaining text
                    if (lastIndex < text.length) {
                        fragments.push({
                            text: text.substring(lastIndex),
                            highlight: false
                        });
                    }
                    
                    // Create new HTML
                    const wrapper = document.createElement('span');
                    fragments.forEach(fragment => {
                        if (fragment.highlight) {
                            const span = document.createElement('span');
                            span.className = 'search-highlight';
                            span.textContent = fragment.text;
                            wrapper.appendChild(span);
                        } else {
                            wrapper.appendChild(document.createTextNode(fragment.text));
                        }
                    });
                    
                    node.parentNode.replaceChild(wrapper, node);
                }
            } else if (node.nodeType === Node.ELEMENT_NODE && 
                       node.nodeName !== 'SCRIPT' && 
                       node.nodeName !== 'STYLE') {
                Array.from(node.childNodes).forEach(child => highlightNode(child));
            }
        }
        
        highlightNode(element);
    }

    function normalizeText(text) {
        return text.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
    }

});

// Function to update the counter
function updateCounter() {
    const counterDiv = document.getElementById('product-counter');
    const totalCards = document.querySelectorAll('.product-card').length;
    const visibleCards = document.querySelectorAll('.product-card:not([style*="display: none"]):not(.hidden)').length;
    counterDiv.textContent = `Showing ${visibleCards} of ${totalCards} products`;
}

