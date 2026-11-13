// Platinum Painting homepage installer (run once via Atarim execute-php). Idempotent: re-running updates the same posts.
$BASE = '__BASE__';
$log  = array();
$get  = function ( $path ) use ( $BASE ) {
	$r = wp_remote_get( $BASE . $path, array( 'timeout' => 30 ) );
	if ( is_wp_error( $r ) || 200 !== wp_remote_retrieve_response_code( $r ) ) {
		throw new Exception( 'fetch failed: ' . $path );
	}
	return wp_remote_retrieve_body( $r );
};
$admins = get_users( array( 'role' => 'administrator', 'number' => 1, 'orderby' => 'ID' ) );
if ( $admins ) { wp_set_current_user( $admins[0]->ID ); }

// 1. Child theme files ---------------------------------------------------------
$tdir = get_stylesheet_directory();
if ( basename( $tdir ) !== 'platinum-painting' ) { throw new Exception( 'unexpected active theme ' . $tdir ); }
if ( file_exists( $tdir . '/functions.php' ) && ! file_exists( $tdir . '/functions.php.orig' ) ) {
	copy( $tdir . '/functions.php', $tdir . '/functions.php.orig' );
}
wp_mkdir_p( $tdir . '/assets' );
file_put_contents( $tdir . '/functions.php', $get( 'build/theme/functions.php' ) );
file_put_contents( $tdir . '/assets/pp.css', $get( 'build/theme/assets/pp.css' ) );
file_put_contents( $tdir . '/assets/pp.js', $get( 'build/theme/assets/pp.js' ) );
update_option( 'pp_hero_image_id', 15 );
$log[] = 'theme files written';

// 2. Primary menu (custom links, per the supplied sitemap) ----------------------
$menu = wp_get_nav_menu_object( 'primary-menu' );
$menu_id = $menu ? $menu->term_id : wp_create_nav_menu( 'Primary Menu' );
if ( ! $menu ) { wp_update_term( $menu_id, 'nav_menu', array( 'slug' => 'primary-menu' ) ); }
foreach ( (array) wp_get_nav_menu_items( $menu_id ) as $it ) { wp_delete_post( $it->ID, true ); }
foreach ( json_decode( $get( 'build/out/nav.json' ), true ) as $i => $n ) {
	wp_update_nav_menu_item( $menu_id, 0, array( 'menu-item-title' => $n[0], 'menu-item-url' => ( '/' === $n[1] ? home_url( '/' ) : home_url( $n[1] ) ), 'menu-item-status' => 'publish', 'menu-item-position' => $i + 1, 'menu-item-type' => 'custom' ) );
}
$locs = get_theme_mod( 'nav_menu_locations', array() );
$locs['menu-1'] = $menu_id;
set_theme_mod( 'nav_menu_locations', $locs );
$log[] = 'menu ' . $menu_id;

// 3. Contact Form 7 form -------------------------------------------------------
$cf7_id = (int) get_option( 'pp_cf7_form_id' );
$cf = $cf7_id ? wpcf7_contact_form( $cf7_id ) : null;
if ( ! $cf ) { $cf = WPCF7_ContactForm::get_template(); }
$form = '<div class="pp-f-row"><label><span class="pp-sr">Name</span>[text* your-name autocomplete:name placeholder "Name"]</label><label><span class="pp-sr">Phone</span>[tel your-phone autocomplete:tel placeholder "Phone"]</label></div>' . "\n"
	. '<label><span class="pp-sr">Email</span>[email* your-email autocomplete:email placeholder "Email"]</label>' . "\n"
	. '<label><span class="pp-sr">Service</span>[select your-service "Interior House Painting" "Exterior House Painting" "Commercial Painting" "Strata / Body Corp Painting" "Roof Restorations" "Render Coatings" "Timber Decks & Pergolas" "Colour Consultation"]</label>' . "\n"
	. '<label><span class="pp-sr">Tell us about your project</span>[textarea your-message x3 placeholder "Tell us about your project"]</label>' . "\n"
	. '[submit "Request My Free Quote"]';
$domain = wp_parse_url( home_url(), PHP_URL_HOST );
$cf->set_title( 'Homepage Quote Form' );
$cf->set_properties( array(
	'form' => $form,
	'mail' => array(
		'active' => true, 'recipient' => 'test@gmail.com',
		'sender' => 'Platinum Painting Website <wordpress@' . $domain . '>',
		'subject' => 'Free quote request: [your-service]',
		'body' => "Name: [your-name]\nPhone: [your-phone]\nEmail: [your-email]\nService: [your-service]\n\nProject details:\n[your-message]\n\n--\nSent from the homepage quote form on " . home_url( '/' ),
		'additional_headers' => 'Reply-To: [your-email]', 'attachments' => '', 'use_html' => false, 'exclude_blank' => false,
	),
	'mail_2' => array_merge( $cf->prop( 'mail_2' ), array( 'active' => false ) ),
	'messages' => array_merge( (array) $cf->prop( 'messages' ), array( 'mail_sent_ok' => "Thanks, we've got it. We'll be in touch within one business day to book your inspection." ) ),
) );
$cf7_id = $cf->save();
update_option( 'pp_cf7_form_id', $cf7_id );
$log[] = 'cf7 ' . $cf7_id;

// 4. Elementor kit globals (brand colours + fonts) -------------------------------
$kit_id = (int) get_option( 'elementor_active_kit' );
if ( $kit_id ) {
	$ks = get_post_meta( $kit_id, '_elementor_page_settings', true );
	$ks = is_array( $ks ) ? $ks : array();
	$ks['system_colors'] = array(
		array( '_id' => 'primary', 'title' => 'Primary (Blue)', 'color' => '#1359AC' ),
		array( '_id' => 'secondary', 'title' => 'Secondary (Navy)', 'color' => '#0B2B55' ),
		array( '_id' => 'text', 'title' => 'Text', 'color' => '#3A3D42' ),
		array( '_id' => 'accent', 'title' => 'Ink', 'color' => '#0E0E10' ),
	);
	$ks['custom_colors'] = array(
		array( '_id' => 'ppmist', 'title' => 'Mist', 'color' => '#E3ECF7' ),
		array( '_id' => 'ppgrey', 'title' => 'Grey', 'color' => '#C8CDD3' ),
		array( '_id' => 'ppbg', 'title' => 'Light background', 'color' => '#F3F5F8' ),
		array( '_id' => 'ppline', 'title' => 'Line', 'color' => '#E3E7EC' ),
	);
	$ks['system_typography'] = array(
		array( '_id' => 'primary', 'title' => 'Headings (Cinzel)', 'typography_typography' => 'custom', 'typography_font_family' => 'Cinzel', 'typography_font_weight' => '600' ),
		array( '_id' => 'secondary', 'title' => 'Accent (Cormorant Garamond)', 'typography_typography' => 'custom', 'typography_font_family' => 'Cormorant Garamond', 'typography_font_weight' => '500', 'typography_font_style' => 'italic' ),
		array( '_id' => 'text', 'title' => 'Body (Figtree)', 'typography_typography' => 'custom', 'typography_font_family' => 'Figtree', 'typography_font_weight' => '400' ),
		array( '_id' => 'accent', 'title' => 'Buttons (Figtree)', 'typography_typography' => 'custom', 'typography_font_family' => 'Figtree', 'typography_font_weight' => '600' ),
	);
	$ks['body_color'] = '#0E0E10';
	$ks['body_typography_typography'] = 'custom';
	$ks['body_typography_font_family'] = 'Figtree';
	$ks['link_normal_color'] = '#1359AC';
	$ks['link_hover_color'] = '#0B2B55';
	$ks['body_background_background'] = 'classic';
	$ks['body_background_color'] = '#FFFFFF';
	$ks['hello_header_footer'] = '';
	update_post_meta( $kit_id, '_elementor_page_settings', $ks );
	$log[] = 'kit ' . $kit_id;
}
update_option( 'elementor_disable_color_schemes', 'yes' );
update_option( 'elementor_disable_typography_schemes', 'yes' );

// 5. Elementor documents ----------------------------------------------------------
$save_doc = function ( $post_id, $json_path, $replace = array() ) use ( $get ) {
	$raw = $get( $json_path );
	foreach ( $replace as $k => $v ) { $raw = str_replace( $k, $v, $raw ); }
	$data = json_decode( $raw, true );
	if ( ! is_array( $data ) ) { throw new Exception( 'bad json ' . $json_path ); }
	$doc = \Elementor\Plugin::$instance->documents->get( $post_id, false );
	$ok = $doc->save( array( 'elements' => $data ) );
	if ( ! $ok ) { // fallback: direct meta (same format the editor writes)
		update_post_meta( $post_id, '_elementor_edit_mode', 'builder' );
		update_post_meta( $post_id, '_elementor_version', ELEMENTOR_VERSION );
		update_post_meta( $post_id, '_elementor_data', wp_slash( wp_json_encode( $data ) ) );
	}
	return $ok ? 'saved' : 'meta-fallback';
};
$find = function ( $type, $key ) {
	$q = get_posts( array( 'post_type' => $type, 'post_status' => 'any', 'meta_key' => '_pp_build', 'meta_value' => $key, 'numberposts' => 1, 'fields' => 'ids' ) );
	return $q ? (int) $q[0] : 0;
};

// Home page
$home_id = $find( 'page', 'home' );
if ( ! $home_id ) {
	$home_id = wp_insert_post( array( 'post_type' => 'page', 'post_status' => 'publish', 'post_title' => 'Home', 'post_name' => 'home' ) );
	update_post_meta( $home_id, '_pp_build', 'home' );
}
update_post_meta( $home_id, '_wp_page_template', 'elementor_header_footer' );
update_post_meta( $home_id, '_elementor_edit_mode', 'builder' );
update_post_meta( $home_id, '_elementor_template_type', 'wp-page' );
$log[] = 'home ' . $home_id . ' ' . $save_doc( $home_id, 'build/out/home.json', array( '__CF7_ID__' => $cf7_id ) );

// UAE header + footer templates
foreach ( array( 'header' => 'type_header', 'footer' => 'type_footer' ) as $k => $type ) {
	$id = $find( 'elementor-hf', $k );
	if ( ! $id ) {
		$id = wp_insert_post( array( 'post_type' => 'elementor-hf', 'post_status' => 'publish', 'post_title' => 'Site ' . ucfirst( $k ) ) );
		update_post_meta( $id, '_pp_build', $k );
	}
	update_post_meta( $id, 'ehf_template_type', $type );
	update_post_meta( $id, 'ehf_target_include_locations', array( 'rule' => array( 'basic-global' ), 'specific' => array() ) );
	update_post_meta( $id, 'ehf_target_exclude_locations', array() );
	update_post_meta( $id, 'ehf_target_user_roles', array( 'all' ) );
	update_post_meta( $id, '_wp_page_template', 'elementor_canvas' );
	update_post_meta( $id, '_elementor_edit_mode', 'builder' );
	update_post_meta( $id, '_elementor_template_type', 'wp-post' );
	$log[] = $k . ' ' . $id . ' ' . $save_doc( $id, 'build/out/' . $k . '.json' );
}

// 6. Front page + Yoast homepage SEO --------------------------------------------
update_option( 'show_on_front', 'page' );
update_option( 'page_on_front', $home_id );
update_post_meta( $home_id, '_yoast_wpseo_title', 'Gold Coast Painters | Platinum Painting Gold Coast' );
update_post_meta( $home_id, '_yoast_wpseo_metadesc', 'Gold Coast painters for homes, businesses and strata. Coatings built for sun, salt and storms, with free on-site quotes that are written and itemised.' );
update_post_meta( $home_id, '_yoast_wpseo_focuskw', 'Gold Coast painters' );

// 7. Rebuild Elementor CSS --------------------------------------------------------
\Elementor\Plugin::$instance->files_manager->clear_cache();
if ( function_exists( 'wp_cache_flush' ) ) { wp_cache_flush(); }

return implode( ' | ', $log ) . ' | front=' . get_option( 'page_on_front' );
