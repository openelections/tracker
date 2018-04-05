import base64
import os

import betamax
from betamax.cassette import cassette


def sanitize_token(interaction, current_cassette):
    headers = interaction.data['request']['headers']
    token = headers.get('Authorization')[0]
    # Create a new placeholder so that when cassette is saved,
    # Betamax will replace the token with our placeholder.
    current_cassette.placeholders.append(
        cassette.Placeholder(placeholder='Bearer <GITHUB-USER-TOKEN>', replace=token)
    )


with betamax.Betamax.configure() as config:
    config.cassette_library_dir = 'tests/cassettes/'
    # Santize user token
    gh_user_token = os.environ['OPENELEX_GITHUB_ACCESS_TOKEN']
    encoded_token = base64.b64encode('{0}'.format(gh_user_token).encode('utf-8'))
    config.define_cassette_placeholder(
        'Bearer <GITHUB-USER-TOKEN>',
        encoded_token.decode('utf-8')
    )
    config.before_record(callback=sanitize_token)
