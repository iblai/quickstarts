
# OAuth2 Guide

This guide will walk you through how to obtain a Client ID, Client Secret, Grant Type, and additional authentication details for different platforms.

## ibl-dm-pro (Base Manager)

### OAuth2 Provider
To create, update, or edit an application:
- Navigate to: https://base.manager.example.com/admin/oauth2_provider/application/

## ibl-edx-pro (Learning Management System)

### OAuth2 Provider
To create, update, or edit an application:
- Navigate to: https://learn.example.com/admin/oauth2_provider/application/

### OpenID Connect
To create, update, or edit an application:
- Navigate to: https://learn.example.com/admin/oidc_provider/client/

## Cross-Platform Credentials

### ibl-edx-pro to ibl-dm-pro credentials
To view the credentials:
- Navigate to: https://learn.example.com/admin/ibl_api_auth/oauthcredentials/
- Look for an application called 'manager'

### ibl-dm-pro to ibl-edx-pro credentials
To view the credentials:
- Navigate to: https://base.manager.example.com/admin/core/oauthcredentials/
- Look for an application called 'edx'


## Single Sign-On (SSO) with Third-Party Configurations

### Learning Management System (ibl-edx-pro)

To configure SSO with third-party providers:

1. Navigate to: https://learn.example.com/admin/third_party_auth/oauth2providerconfig/

2. Here you can add, edit, or manage OAuth2 provider configurations for SSO.

Note: Ensure you have the correct OAuth2 credentials from the third-party provider before setting up the configuration. Also, make sure to set the correct callback URL in the third-party provider's settings, which typically would be:
https://learn.example.com/auth/complete/{provider_slug}/

Remember to test the SSO configuration thoroughly in a staging environment before deploying to production.


Note: Ensure you have the necessary permissions to access these administrative areas.

