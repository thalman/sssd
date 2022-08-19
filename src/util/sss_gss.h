/*
    Authors:
        Tomas Halman <thalman@redhat.com>

    Copyright (C) 2022 Red Hat

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#ifndef _SSS_GSS_H_
#define _SSS_GSS_H_

#include <talloc.h>
#include <gssapi.h>
#include <errno.h>

#include "util/util.h"

char *sss_gss_error_message(TALLOC_CTX *ctx, OM_uint32 status_code);

char *sss_gss_get_principal_from_creds(TALLOC_CTX *ctx, gss_cred_id_t creds);

errno_t sss_gss_get_creds(TALLOC_CTX *ctx,
                          const char *principal,
                          const char *realm,
                          OM_uint32 lifetime,
                          bool canonicalize,
                          const char *keytab_name,
                          gss_cred_id_t *_creds,
                          char **_principal,
                          OM_uint32 *_lifetime_out);

errno_t sss_gss_find_host_creds(TALLOC_CTX *ctx,
                                const char *hostname,
                                const char *realm,
                                bool canonicalize,
                                int lifetime,
                                const char *keytab_name,
                                gss_cred_id_t *_creds,
                                char **_principal,
                                OM_uint32 *_lifetime);


#endif /* _SSS_GSS_H_ */
