import unittest

from ytauthdownloader.core import AuthorizationRequired, build_download_command, validate_video_url


class ValidateVideoUrlTests(unittest.TestCase):
    def test_accepts_a_single_https_watch_url_and_canonicalizes_it(self):
        self.assertEqual(
            validate_video_url('https://www.youtube.com/watch?v=abc123XYZ_9'),
            'https://www.youtube.com/watch?v=abc123XYZ_9',
        )

    def test_rejects_playlist_and_deceptive_hosts(self):
        for url in (
            'https://www.youtube.com/watch?v=abc123XYZ_9&list=PL123',
            'https://youtube.com.evil.example/watch?v=abc123XYZ_9',
            'https://attacker@youtube.com/watch?v=abc123XYZ_9',
        ):
            with self.assertRaises(ValueError):
                validate_video_url(url)


class CommandTests(unittest.TestCase):
    def test_requires_authorization_acknowledgement(self):
        with self.assertRaises(AuthorizationRequired):
            build_download_command('https://youtu.be/abc123XYZ_9', authorized=False)

    def test_builds_a_single_video_mp3_command_without_configs_or_plugins(self):
        command = build_download_command('https://youtu.be/abc123XYZ_9', authorized=True, audio_only=True, output_dir='downloads')
        self.assertIn('--ignore-config', command)
        self.assertIn('--no-playlist', command)
        self.assertIn('--no-plugins', command)
        self.assertIn('--extract-audio', command)
        self.assertEqual(command[-2:], ['--', 'https://www.youtube.com/watch?v=abc123XYZ_9'])


if __name__ == '__main__':
    unittest.main()
