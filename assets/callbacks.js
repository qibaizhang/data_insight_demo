/**
 * DataInsight Client-side Callbacks
 *
 * Handles SSE streaming response updates with simplified data format.
 * Uses uuid-based change detection for efficient updates.
 */

window.dash_clientside = Object.assign({}, window.dash_clientside, {
    datainsight: {
        // Track last processed uuid to avoid duplicate processing
        _lastUuid: null,
        // Accumulated content
        _fullContent: '',
        // Flag to track if stream is active
        _streamActive: false,
        // Track if infographic was received (prioritize over markdown)
        _hasInfographic: false,

        /**
         * Update streaming response content
         * Accumulates content and updates the FefferyMarkdown component
         */
        updateStreamingResponse: function(data, currentContent) {
            if (!data) {
                return window.dash_clientside.no_update;
            }

            try {
                // Parse data
                let parsed;
                if (typeof data === 'string') {
                    parsed = JSON.parse(data);
                } else if (typeof data === 'object') {
                    parsed = data;
                } else {
                    return window.dash_clientside.no_update;
                }

                // Skip if already processed (same uuid)
                if (parsed.uuid && parsed.uuid === this._lastUuid) {
                    return window.dash_clientside.no_update;
                }
                this._lastUuid = parsed.uuid;

                // Handle content - accumulate text
                if ('content' in parsed) {
                    // If this is the first content and stream wasn't active, reset
                    if (!this._streamActive) {
                        this._fullContent = '';
                        this._streamActive = true;
                        this._hasInfographic = false;  // Reset infographic flag
                        console.log('[SSE] Stream started');
                    }
                    this._fullContent += parsed.content;
                    // Log every 500 chars to avoid too much output
                    if (this._fullContent.length % 500 < parsed.content.length) {
                        console.log('[SSE] Content accumulated, total length:', this._fullContent.length);
                    }
                    return this._fullContent;
                }

                // Handle chart data - don't interrupt content display
                if ('chart' in parsed) {
                    console.log('[SSE] Chart received');
                    window.dash_clientside.set_props('chart-config-store', { data: parsed.chart });
                    window.dash_clientside.set_props('display-tabs', { activeKey: 'chart' });
                    return window.dash_clientside.no_update;
                }

                // Handle query data - don't interrupt content display
                if ('data' in parsed) {
                    console.log('[SSE] Data received, rows:', parsed.data.data ? parsed.data.data.length : 0);
                    window.dash_clientside.set_props('query-result-store', { data: parsed.data });
                    window.dash_clientside.set_props('display-tabs', { activeKey: 'data' });
                    return window.dash_clientside.no_update;
                }

                // Handle report - prioritize infographic over markdown
                if ('report' in parsed) {
                    const reportFormat = parsed.report.format;
                    const reportContent = parsed.report.content;
                    console.log('[SSE] Report received, format:', reportFormat, 'length:', reportContent.length);

                    // If this is an infographic, always update and mark flag
                    if (reportFormat === 'infographic') {
                        this._hasInfographic = true;
                        window.dash_clientside.set_props('report-content-store', { data: reportContent });
                        window.dash_clientside.set_props('display-tabs', { activeKey: 'report' });
                        console.log('[SSE] Infographic report set');
                    }
                    // If this is markdown, only update if no infographic was received
                    else if (!this._hasInfographic) {
                        window.dash_clientside.set_props('report-content-store', { data: reportContent });
                        window.dash_clientside.set_props('display-tabs', { activeKey: 'report' });
                        console.log('[SSE] Markdown report set');
                    } else {
                        console.log('[SSE] Markdown report skipped (infographic already received)');
                    }
                    return window.dash_clientside.no_update;
                }

                // Handle complete signal
                if ('complete' in parsed) {
                    // Use fullContent from server if available (more reliable)
                    const finalContent = parsed.fullContent || this._fullContent;
                    console.log('[SSE] Stream complete, final content length:', finalContent.length);

                    // Stop SSE connection
                    window.dash_clientside.set_props('chat-sse-source', {
                        immediate: false,
                        url: ''
                    });

                    // Hide loading indicator
                    window.dash_clientside.set_props('chat-loading-indicator', {
                        style: { display: 'none' }
                    });

                    // Trigger finalization with the full content
                    if (finalContent && finalContent.length > 0) {
                        window.dash_clientside.set_props('assistant-response-store', {
                            data: finalContent
                        });
                    }

                    // Reset for next stream
                    this._fullContent = '';
                    this._lastUuid = null;
                    this._streamActive = false;
                    this._hasInfographic = false;

                    return finalContent || window.dash_clientside.no_update;
                }

                // Handle error
                if ('error' in parsed) {
                    console.error('[SSE] Error:', parsed.error);

                    window.dash_clientside.set_props('chat-sse-source', {
                        immediate: false,
                        url: ''
                    });
                    window.dash_clientside.set_props('chat-loading-indicator', {
                        style: { display: 'none' }
                    });

                    // Reset state
                    this._fullContent = '';
                    this._lastUuid = null;
                    this._streamActive = false;
                    this._hasInfographic = false;

                    return `**错误**: ${parsed.error}`;
                }

            } catch (e) {
                console.error('[SSE] Error parsing data:', e, 'Raw:', data);
            }

            return window.dash_clientside.no_update;
        }
    }
});
