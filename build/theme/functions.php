<?php
/**
 * Platinum Painting – Hello Elementor child theme.
 */
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'PP_CHILD_VERSION', '1.0.0' );

/**
 * Child stylesheet + homepage helper CSS/JS.
 */
add_action( 'wp_enqueue_scripts', function () {
	$dir = get_stylesheet_directory();
	$uri = get_stylesheet_directory_uri();

	wp_enqueue_style( 'platinum-painting-child', get_stylesheet_uri(), array(), PP_CHILD_VERSION );
	wp_enqueue_style( 'pp-site', $uri . '/assets/pp.css', array( 'platinum-painting-child' ), (string) filemtime( $dir . '/assets/pp.css' ) );
	wp_enqueue_script( 'pp-site', $uri . '/assets/pp.js', array(), (string) filemtime( $dir . '/assets/pp.js' ), array( 'in_footer' => true, 'strategy' => 'defer' ) );
}, 20 );

/**
 * Preload the hero background (the above-the-fold image) on the front page.
 */
add_action( 'wp_head', function () {
	if ( ! is_front_page() ) {
		return;
	}
	$id = (int) get_option( 'pp_hero_image_id' );
	if ( $id ) {
		$src = wp_get_attachment_image_url( $id, 'full' );
		if ( $src ) {
			echo '<link rel="preload" as="image" href="' . esc_url( $src ) . '" fetchpriority="high">' . "\n";
		}
	}
}, 1 );

/**
 * Keep Contact Form 7 markup clean (no auto <p>/<br>), so the form follows the design grid.
 */
add_filter( 'wpcf7_autop_or_not', '__return_false' );
