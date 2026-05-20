<?php
/**
 * Plugin Name: Paulo AI Resume Chatbot
 * Description: AI chatbot powered by Python + Gemini (Free). Answers questions about Paulo's resume.
 * Version: 2.0
 * Author: Jose Paulo Timbang
 */

if (!defined('ABSPATH')) exit;

class PauloAIChatbot {

    public function __construct() {
        add_action('wp_enqueue_scripts', [$this, 'enqueue_assets']);
        add_action('wp_footer', [$this, 'render_chatbot_html']);
        add_action('admin_menu', [$this, 'add_settings_page']);
        add_action('admin_init', [$this, 'register_settings']);
    }

    public function enqueue_assets() {
        wp_enqueue_style('paulo-chatbot-css',
            plugin_dir_url(__FILE__) . 'chat-widget.css', [], '2.0');
        wp_enqueue_script('paulo-chatbot-js',
            plugin_dir_url(__FILE__) . 'chat-widget.js', [], '2.0', true);

        // Pass the Python server URL to JavaScript
        $server_url = get_option('paulo_chatbot_server_url', 'http://localhost:5000');
        wp_localize_script('paulo-chatbot-js', 'pauloChatbot', [
            'server_url' => trailingslashit($server_url) . 'chat',
        ]);
    }

    public function render_chatbot_html() {
        echo '<div id="paulo-chatbot-wrapper">
            <div id="paulo-chat-window">
                <div id="paulo-chat-header">
                    <div id="paulo-chat-header-info">
                        <div id="paulo-chat-avatar">P</div>
                        <div>
                            <div id="paulo-chat-name">Paulo\'s AI Assistant</div>
                            <div id="paulo-chat-status"><span id="paulo-status-dot"></span> Online</div>
                        </div>
                    </div>
                    <button id="paulo-chat-close" aria-label="Close chat">✕</button>
                </div>
                <div id="paulo-chat-messages"></div>
                <div id="paulo-chat-input-area">
                    <input type="text" id="paulo-chat-input" placeholder="Ask about Paulo\'s skills, experience..." autocomplete="off" />
                    <button id="paulo-chat-send" aria-label="Send message">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                            <line x1="22" y1="2" x2="11" y2="13"></line>
                            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                        </svg>
                    </button>
                </div>
            </div>
            <button id="paulo-chat-toggle" aria-label="Open chat">
                <span id="paulo-toggle-icon-open">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                    </svg>
                </span>
                <span id="paulo-toggle-icon-close" style="display:none;">✕</span>
            </button>
        </div>';
    }

    public function add_settings_page() {
        add_options_page('Paulo AI Chatbot', 'AI Chatbot', 'manage_options',
            'paulo-chatbot', [$this, 'settings_page_html']);
    }

    public function register_settings() {
        register_setting('paulo_chatbot_settings', 'paulo_chatbot_server_url');
    }

    public function settings_page_html() { ?>
        <div class="wrap">
            <h1>Paulo AI Chatbot Settings</h1>
            <form method="post" action="options.php">
                <?php settings_fields('paulo_chatbot_settings'); ?>
                <table class="form-table">
                    <tr>
                        <th>Python Server URL</th>
                        <td>
                            <input type="text" name="paulo_chatbot_server_url"
                                value="<?php echo esc_attr(get_option('paulo_chatbot_server_url', 'http://localhost:5000')); ?>"
                                style="width:400px" placeholder="https://your-server.com" />
                            <p class="description">
                                The URL where your Python Flask server is running.<br>
                                Example: <code>https://your-app.onrender.com</code> or <code>http://your-vps-ip:5000</code>
                            </p>
                        </td>
                    </tr>
                </table>
                <?php submit_button(); ?>
            </form>
            <hr>
            <h2>Setup Instructions</h2>
            <ol>
                <li>Deploy your Python server (see README for free hosting options)</li>
                <li>Enter the server URL above and save</li>
                <li>Visit your site — the chat bubble will appear bottom-right</li>
            </ol>
        </div>
    <?php }
}

new PauloAIChatbot();
