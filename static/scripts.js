document.addEventListener('DOMContentLoaded', () => {
    const filterInputs = document.querySelectorAll('.filter-checkbox, .filter-range-min, .filter-range-max');

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
                    const rangeMatch = cardAttrValue.match(/(\d{4})\s*[-:]\s*(\d{4})/);
                    if (rangeMatch) {
                        const cardStart = parseInt(rangeMatch[1], 10);
                        const cardEnd = parseInt(rangeMatch[2], 10);
                        // Check for overlap between card's range and filter's range
                        if (cardEnd < filterValue.min || cardStart > filterValue.max) {
                            isVisible = false;
                            break;
                        }
                    } else {
                        isVisible = false;
                        break;
                    }
                }
            }

            card.style.display = isVisible ? '' : 'none';
        });
    }

    filterInputs.forEach(input => {
        input.addEventListener('change', filterProducts);
    });

    // Initial filter on page load
    filterProducts();
});