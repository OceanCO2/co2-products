document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.product-card');
    cards.forEach(card => {
        card.addEventListener('click', function(event) {
            // Prevent flip if clicking on link
            if (event.target.tagName !== 'A') {
                this.classList.toggle('flipped');
            }
        });
    });

    const filterInputs = document.querySelectorAll('.filter-checkbox, .filter-radio, .filter-slider-min, .filter-slider-max');
    const periodSliderState = new Map();
    const PERIOD_TRACK_COLOR = '#d0d7de';
    const PERIOD_SELECTION_COLOR = '#0d6efd';

    function updatePeriodSliderSpans(filter) {
        const slider = periodSliderState.get(filter);
        if (!slider) return;
        const { minInput, maxInput, minSpan, maxSpan } = slider;
        if (minSpan && minInput) {
            minSpan.textContent = minInput.value;
        }
        if (maxSpan && maxInput) {
            maxSpan.textContent = maxInput.value;
        }
    }

    function updatePeriodSliderZ(filter) {
        const slider = periodSliderState.get(filter);
        if (!slider) return;
        const { minInput, maxInput } = slider;
        if (!minInput || !maxInput) return;
        const minVal = parseInt(minInput.value, 10);
        const maxVal = parseInt(maxInput.value, 10);
        maxInput.style.zIndex = '4';
        minInput.style.zIndex = minVal >= maxVal ? '5' : '3';
    }

    function updatePeriodSliderBackground(filter) {
        const slider = periodSliderState.get(filter);
        if (!slider || !slider.minInput || !slider.maxInput) return;
        const { minInput, maxInput, rangeMin, rangeMax } = slider;
        if (!Number.isFinite(rangeMin) || !Number.isFinite(rangeMax) || rangeMax === rangeMin) {
            return;
        }
        const minValue = parseInt(minInput.value, 10);
        const maxValue = parseInt(maxInput.value, 10);
        if (Number.isNaN(minValue) || Number.isNaN(maxValue)) {
            return;
        }
        const lower = Math.min(minValue, maxValue);
        const upper = Math.max(minValue, maxValue);
        const minPercent = ((lower - rangeMin) / (rangeMax - rangeMin)) * 100;
        const maxPercent = ((upper - rangeMin) / (rangeMax - rangeMin)) * 100;
        const background = `linear-gradient(to right, ${PERIOD_TRACK_COLOR} ${minPercent}%, ${PERIOD_SELECTION_COLOR} ${minPercent}%, ${PERIOD_SELECTION_COLOR} ${maxPercent}%, ${PERIOD_TRACK_COLOR} ${maxPercent}%)`;
        minInput.style.background = background;
        maxInput.style.background = background;
    }

    function refreshPeriodSlider(filter) {
        updatePeriodSliderSpans(filter);
        updatePeriodSliderZ(filter);
        updatePeriodSliderBackground(filter);
    }

    function extractTokenList(value) {
        if (!value) return [];
        return value.split('||').map(token => token.trim()).filter(Boolean);
    }

    document.querySelectorAll('.period-slider-wrapper').forEach(wrapper => {
        const filterName = wrapper.dataset.filter;
        const minInput = wrapper.querySelector('.filter-slider-min');
        const maxInput = wrapper.querySelector('.filter-slider-max');
        const minSpan = minInput ? document.getElementById(`${minInput.id}-value`) : null;
        const maxSpan = maxInput ? document.getElementById(`${maxInput.id}-value`) : null;
        const rangeMin = minInput ? parseInt(minInput.min, 10) : null;
        const rangeMax = maxInput ? parseInt(maxInput.max, 10) : null;
        if (minInput) {
            minInput.classList.add('range-active');
            minInput.style.zIndex = '3';
        }
        if (maxInput) {
            maxInput.classList.add('range-active');
            maxInput.style.zIndex = '4';
        }
        periodSliderState.set(filterName, {
            wrapper,
            minInput,
            maxInput,
            minSpan,
            maxSpan,
            rangeMin,
            rangeMax
        });
        refreshPeriodSlider(filterName);
    });

    filterInputs.forEach(input => {
        input.addEventListener('input', filterProducts);
        input.addEventListener('change', filterProducts);
        if (input.classList.contains('filter-slider-min')) {
            input.addEventListener('input', function() {
                if (this.dataset.filterType === 'period') {
                    const filter = this.dataset.filter;
                    const slider = periodSliderState.get(filter);
                    if (slider && slider.maxInput) {
                        const minVal = parseInt(this.value, 10);
                        const maxVal = parseInt(slider.maxInput.value, 10);
                        if (!Number.isNaN(minVal) && !Number.isNaN(maxVal) && minVal > maxVal) {
                            slider.maxInput.value = this.value;
                        }
                        refreshPeriodSlider(filter);
                    }
                } else {
                    const span = document.getElementById(this.id.replace('-min', '') + '-min-value');
                    if (span) span.textContent = this.value;
                }
            });
        }
        if (input.classList.contains('filter-slider-max')) {
            input.addEventListener('input', function() {
                if (this.dataset.filterType === 'period') {
                    const filter = this.dataset.filter;
                    const slider = periodSliderState.get(filter);
                    if (slider && slider.minInput) {
                        const maxVal = parseInt(this.value, 10);
                        const minVal = parseInt(slider.minInput.value, 10);
                        if (!Number.isNaN(minVal) && !Number.isNaN(maxVal) && maxVal < minVal) {
                            slider.minInput.value = this.value;
                        }
                        refreshPeriodSlider(filter);
                    }
                } else {
                    const span = document.getElementById(this.id.replace('-max', '') + '-max-value');
                    if (span) span.textContent = this.value;
                }
            });
        }
    });

    function filterProducts() {
        const activeFilters = {};
        const ensureFilter = (filter, type) => {
            if (!activeFilters[filter]) {
                if (type === 'period') {
                    const slider = periodSliderState.get(filter);
                    const minInput = slider?.minInput;
                    const maxInput = slider?.maxInput;
                    const selectedMin = minInput ? parseInt(minInput.value, 10) : null;
                    const selectedMax = maxInput ? parseInt(maxInput.value, 10) : null;
                    activeFilters[filter] = {
                        type: 'period',
                        options_checked: [],
                        min: selectedMin,
                        max: selectedMax,
                        rangeMin: slider?.rangeMin ?? null,
                        rangeMax: slider?.rangeMax ?? null,
                        sliderActive: false
                    };
                } else if (type === 'checkbox') {
                    activeFilters[filter] = { type: 'checkbox', values: [] };
                } else if (type === 'slider') {
                    activeFilters[filter] = { type: 'slider', min: null, max: null };
                } else {
                    activeFilters[filter] = { type: 'radio', values: [] };
                }
            }
            return activeFilters[filter];
        };

        document.querySelectorAll('.filter-checkbox:checked').forEach(cb => {
            const filter = cb.dataset.filter;
            const filterType = cb.dataset.filterType;
            const entry = ensureFilter(filter, filterType === 'period' ? 'period' : 'checkbox');
            if (entry.type === 'period') {
                entry.options_checked.push(cb.value);
            } else {
                entry.values.push(cb.value);
            }
        });

        document.querySelectorAll('.filter-radio:checked').forEach(rb => {
            const filter = rb.dataset.filter;
            const entry = ensureFilter(filter, 'radio');
            entry.values = [rb.value];
        });

        document.querySelectorAll('.filter-slider-min').forEach(minInput => {
            const filter = minInput.dataset.filter;
            const filterType = minInput.dataset.filterType;
            const maxInput = document.getElementById(minInput.id.replace('-min', '-max'));
            if (!maxInput) {
                return;
            }
            const minVal = filterType === 'period' ? parseInt(minInput.value, 10) : parseFloat(minInput.value);
            const maxVal = filterType === 'period' ? parseInt(maxInput.value, 10) : parseFloat(maxInput.value);
            if (Number.isNaN(minVal) || Number.isNaN(maxVal)) {
                return;
            }
            const entry = ensureFilter(filter, filterType === 'period' ? 'period' : 'slider');
            entry.min = Math.min(minVal, maxVal);
            entry.max = Math.max(minVal, maxVal);
            if (entry.type === 'period') {
                const slider = periodSliderState.get(filter);
                if (slider) {
                    entry.rangeMin = slider.rangeMin;
                    entry.rangeMax = slider.rangeMax;
                    const hasMinRange = Number.isFinite(entry.rangeMin);
                    const hasMaxRange = Number.isFinite(entry.rangeMax);
                    entry.sliderActive = (hasMinRange && entry.min > entry.rangeMin) || (hasMaxRange && entry.max < entry.rangeMax);
                }
            }
        });

        cards.forEach(card => {
            let show = true;
            for (const [filter, config] of Object.entries(activeFilters)) {
                const dataAttr = 'data-' + filter.toLowerCase().replace(/ /g, '-');
                const valueRaw = (card.getAttribute(dataAttr) || '').trim();
                if (config.type === 'checkbox') {
                    if (config.values.length > 0) {
                        const valueTokens = extractTokenList(valueRaw);
                        const matches = config.values.some(val => valueTokens.includes(val));
                        if (!matches) {
                            show = false;
                            break;
                        }
                    }
                } else if (config.type === 'radio') {
                    if (config.values.length > 0) {
                        const valueTokens = extractTokenList(valueRaw);
                        if (!valueTokens.includes(config.values[0])) {
                            show = false;
                            break;
                        }
                    }
                } else if (config.type === 'slider') {
                    if (valueRaw && valueRaw.toLowerCase() !== 'na') {
                        const numericValue = parseFloat(valueRaw);
                        if (Number.isNaN(numericValue) || numericValue < config.min || numericValue > config.max) {
                            show = false;
                            break;
                        }
                    }
                } else if (config.type === 'period') {
                    const sliderActive = !!config.sliderActive;
                    const selectedOptions = config.options_checked || [];
                    if (valueRaw && valueRaw.toLowerCase() !== 'na') {
                        const rangeMatch = valueRaw.match(/^(\d{3,4})\s*-\s*(\d{3,4})$/);
                        if (rangeMatch) {
                            if (sliderActive) {
                                const start = parseInt(rangeMatch[1], 10);
                                const end = parseInt(rangeMatch[2], 10);
                                if (!Number.isFinite(start) || !Number.isFinite(end) ||
                                    (Number.isFinite(config.min) && start > config.min) ||
                                    (Number.isFinite(config.max) && end < config.max)) {
                                    show = false;
                                    break;
                                }
                            }
                        } else {
                            if (selectedOptions.length > 0) {
                                if (!selectedOptions.includes(valueRaw)) {
                                    show = false;
                                    break;
                                }
                            } else if (sliderActive) {
                                show = false;
                                break;
                            }
                        }
                    } else {
                        if (selectedOptions.length > 0 || sliderActive) {
                            show = false;
                            break;
                        }
                    }
                }
            }
            card.style.display = show ? 'block' : 'none';
        });
    }

    filterProducts();
});
