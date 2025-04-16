'use client';

import { useState, memo } from 'react';
import Link from 'next/link';
import { useForm } from 'react-hook-form';
import { ErrorBoundary, FallbackProps } from 'react-error-boundary';
import { FiGlobe, FiGithub, FiTwitter, FiMail, FiHeart, FiArrowUp, FiCheck, FiX } from 'react-icons/fi';
import { trackEvent } from '@/lib/analytics';
import { subscribeToNewsletter } from '@/lib/api';

interface NewsletterFormData {
  email: string;
}

function ErrorFallback({ error, resetErrorBoundary }: FallbackProps) {
  return (
    <div role="alert" className="text-red-500 text-sm">
      <p>Something went wrong:</p>
      <pre>{error.message}</pre>
      <button onClick={resetErrorBoundary} className="text-blue-500 hover:underline">Try again</button>
    </div>
  );
}

const SocialLinks = memo(() => (
  <div className="flex gap-4">
    <a
      href="#"
      className="p-2 text-gray-500 hover:text-blue-600 dark:text-gray-400 dark:hover:text-blue-400 transition-all duration-300 transform hover:-translate-y-1 hover:shadow-lg rounded-full bg-white dark:bg-gray-800"
      aria-label="Twitter"
    >
      <FiTwitter className="w-5 h-5" />
    </a>
    <a
      href="#"
      className="p-2 text-gray-500 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white transition-all duration-300 transform hover:-translate-y-1 hover:shadow-lg rounded-full bg-white dark:bg-gray-800"
      aria-label="GitHub"
    >
      <FiGithub className="w-5 h-5" />
    </a>
    <a
      href="mailto:info@naijanewshub.com"
      className="p-2 text-gray-500 hover:text-red-600 dark:text-gray-400 dark:hover:text-red-400 transition-all duration-300 transform hover:-translate-y-1 hover:shadow-lg rounded-full bg-white dark:bg-gray-800"
      aria-label="Email"
    >
      <FiMail className="w-5 h-5" />
    </a>
  </div>
));

const QuickLinks = memo(() => (
  <div>
    <h3 className="text-sm font-semibold text-gray-900 dark:text-white uppercase tracking-wider mb-4">
      Quick Links
    </h3>
    <ul className="space-y-2">
      <li>
        <Link
          href="/dashboard"
          className="text-sm text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
        >
          Dashboard
        </Link>
      </li>
      <li>
        <Link
          href="/dashboard/articles"
          className="text-sm text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
        >
          Articles
        </Link>
      </li>
      <li>
        <Link
          href="/dashboard/websites"
          className="text-sm text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
        >
          Websites
        </Link>
      </li>
      <li>
        <Link
          href="/dashboard/jobs"
          className="text-sm text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
        >
          Jobs
        </Link>
      </li>
    </ul>
  </div>
));

const NewsletterForm = memo(({ onSubmit, isSubmitting, isSuccess, register, errors }: any) => (
  <form onSubmit={onSubmit} className="space-y-2">
    <div className="relative">
      <input
        type="email"
        {...register('email', {
          required: 'Please enter your email address',
          pattern: {
            value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
            message: 'Please enter a valid email address'
          }
        })}
        placeholder="Your email"
        className={`w-full px-4 py-2 rounded-lg bg-white dark:bg-gray-700 border ${
          errors.email ? 'border-red-500' : 'border-gray-300 dark:border-gray-600'
        } text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 transition-all duration-300`}
        disabled={isSubmitting}
        aria-invalid={errors.email ? 'true' : 'false'}
      />
      {errors.email && (
        <div className="absolute right-3 top-1/2 -translate-y-1/2 text-red-500">
          <FiX className="w-5 h-5" />
        </div>
      )}
    </div>
    {errors.email && (
      <p className="text-xs text-red-500" role="alert">{errors.email.message}</p>
    )}
    <button
      type="submit"
      disabled={isSubmitting}
      className={`w-full px-4 py-2 rounded-lg font-medium transition-all duration-300 ${
        isSubmitting
          ? 'bg-gray-400 dark:bg-gray-600 cursor-not-allowed'
          : 'header-gradient hover:opacity-90 text-white'
      }`}
    >
      {isSubmitting ? (
        <span className="flex items-center justify-center">
          <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Subscribing...
        </span>
      ) : isSuccess ? (
        <span className="flex items-center justify-center">
          <FiCheck className="w-5 h-5 mr-2" />
          Subscribed!
        </span>
      ) : (
        'Subscribe'
      )}
    </button>
  </form>
));

const Footer = memo(() => {
  const currentYear = new Date().getFullYear();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const { register, handleSubmit, formState: { errors }, reset } = useForm<NewsletterFormData>();

  const onSubmit = async (data: NewsletterFormData) => {
    try {
      setIsSubmitting(true);
      trackEvent('newsletter_subscribe_attempt');

      await subscribeToNewsletter(data.email);

      setIsSuccess(true);
      reset();
      trackEvent('newsletter_subscribe_success');

      setTimeout(() => setIsSuccess(false), 3000);
    } catch (err) {
      const error = err instanceof Error ? err : new Error('An unexpected error occurred');
      trackEvent('newsletter_subscribe_error', { error: error.message });
      throw error;
    } finally {
      setIsSubmitting(false);
    }
  };

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
    trackEvent('scroll_to_top_click');
  };

  return (
    <footer className="relative footer-gradient border-t border-gray-700 mt-auto">
      {/* Back to top button */}
      <button
        onClick={scrollToTop}
        className="fixed bottom-4 right-4 p-3 header-gradient text-white rounded-full shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1"
        aria-label="Back to top"
      >
        <FiArrowUp className="w-5 h-5" />
      </button>

      <div className="mx-auto max-w-7xl px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Company Info */}
          <div className="flex flex-col items-center md:items-start">
            <div className="flex items-center gap-2 mb-4">
              <div className="header-gradient p-1 rounded-full">
                <FiGlobe className="w-6 h-6 text-white" />
              </div>
              <span className="text-xl font-bold text-white">
                Naija News Hub
              </span>
            </div>
            <p className="text-sm text-gray-300 text-center md:text-left mb-4">
              Aggregating the latest news from across Nigeria in one convenient location.
            </p>
            <SocialLinks />
          </div>

          {/* Quick Links */}
          <QuickLinks />

          {/* Sitemap */}
          <div>
            <h3 className="text-sm font-semibold text-white uppercase tracking-wider mb-4">
              Sitemap
            </h3>
            <ul className="space-y-2">
              <li>
                <Link
                  href="/about"
                  className="text-sm text-gray-300 hover:text-blue-400 transition-colors"
                >
                  About Us
                </Link>
              </li>
              <li>
                <Link
                  href="/privacy"
                  className="text-sm text-gray-300 hover:text-blue-400 transition-colors"
                >
                  Privacy Policy
                </Link>
              </li>
              <li>
                <Link
                  href="/terms"
                  className="text-sm text-gray-300 hover:text-blue-400 transition-colors"
                >
                  Terms of Service
                </Link>
              </li>
              <li>
                <Link
                  href="/contact"
                  className="text-sm text-gray-300 hover:text-blue-400 transition-colors"
                >
                  Contact Us
                </Link>
              </li>
            </ul>
          </div>

          {/* Newsletter */}
          <div>
            <h3 className="text-sm font-semibold text-white uppercase tracking-wider mb-4">
              Stay Updated
            </h3>
            <p className="text-sm text-gray-300 mb-4">
              Subscribe to our newsletter for the latest news updates.
            </p>
            <ErrorBoundary FallbackComponent={ErrorFallback}>
              <NewsletterForm onSubmit={handleSubmit(onSubmit)} isSubmitting={isSubmitting} isSuccess={isSuccess} register={register} errors={errors} />
            </ErrorBoundary>
          </div>
        </div>

        <div className="border-t border-gray-700 mt-8 pt-8 flex flex-col md:flex-row justify-between items-center gap-4">
          {/* Copyright */}
          <div className="text-sm text-gray-300">
            © {currentYear} Naija News Hub. All rights reserved.
          </div>

          {/* Made with love */}
          <div className="text-sm text-gray-300 flex items-center gap-1">
            Made with <FiHeart className="w-4 h-4 text-red-500 animate-pulse" /> in Nigeria
          </div>

          {/* Version */}
          <div className="text-sm text-gray-300">
            Version 1.0.0
          </div>
        </div>
      </div>
    </footer>
  );
});

export default Footer;