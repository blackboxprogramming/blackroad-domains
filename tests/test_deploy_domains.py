"""
Tests for deploy_domains.py
"""
import sys
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from deploy_domains import deploy_domain, DEPLOYMENTS, PAGES_DIR


class TestDeploymentsConfig:
    """Tests for the DEPLOYMENTS configuration"""

    def test_deployments_not_empty(self):
        """Ensure DEPLOYMENTS dict is not empty"""
        assert len(DEPLOYMENTS) > 0

    def test_all_html_files_have_html_extension(self):
        """All keys should be .html files"""
        for html_file in DEPLOYMENTS.keys():
            assert html_file.endswith('.html'), f"Invalid file: {html_file}"

    def test_all_project_names_are_valid(self):
        """Project names should be lowercase with hyphens only"""
        import re
        pattern = re.compile(r'^[a-z0-9-]+$')
        for project_name in DEPLOYMENTS.values():
            assert pattern.match(project_name), f"Invalid project name: {project_name}"

    def test_no_duplicate_project_names(self):
        """Ensure no two HTML files map to the same project"""
        project_names = list(DEPLOYMENTS.values())
        assert len(project_names) == len(set(project_names)), "Duplicate project names found"

    def test_expected_deployments_exist(self):
        """Verify key deployments are configured"""
        assert "blackroad-io.html" in DEPLOYMENTS
        assert DEPLOYMENTS["blackroad-io.html"] == "blackroad-io"


class TestDeployDomain:
    """Tests for the deploy_domain() function"""

    def test_creates_temp_directory(self):
        """Verify temp directory is created during deployment"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a fake source file
            src_file = os.path.join(tmpdir, "test.html")
            with open(src_file, 'w') as f:
                f.write("<html></html>")

            with patch('deploy_domains.PAGES_DIR', tmpdir):
                with patch('subprocess.run') as mock_run:
                    mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

                    result = deploy_domain("test.html", "test-project")

                    # Verify subprocess was called
                    mock_run.assert_called_once()
                    call_args = mock_run.call_args
                    assert "wrangler" in call_args[0][0]

    def test_copies_html_as_index(self):
        """Ensure HTML file is copied as index.html"""
        with tempfile.TemporaryDirectory() as tmpdir:
            src_file = os.path.join(tmpdir, "source.html")
            with open(src_file, 'w') as f:
                f.write("<html><body>Test Content</body></html>")

            temp_deploy_dir = None

            def capture_cwd(*args, **kwargs):
                nonlocal temp_deploy_dir
                temp_deploy_dir = kwargs.get('cwd')
                # Check index.html exists in cwd
                index_path = os.path.join(temp_deploy_dir, "index.html")
                assert os.path.exists(index_path), "index.html not created"
                with open(index_path) as f:
                    content = f.read()
                assert "Test Content" in content
                return MagicMock(returncode=0, stdout="", stderr="")

            with patch('deploy_domains.PAGES_DIR', tmpdir):
                with patch('subprocess.run', side_effect=capture_cwd):
                    deploy_domain("source.html", "test-project")

    def test_returns_true_on_success(self):
        """Verify function returns True on successful deployment"""
        with tempfile.TemporaryDirectory() as tmpdir:
            src_file = os.path.join(tmpdir, "test.html")
            with open(src_file, 'w') as f:
                f.write("<html></html>")

            with patch('deploy_domains.PAGES_DIR', tmpdir):
                with patch('subprocess.run') as mock_run:
                    mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

                    result = deploy_domain("test.html", "test-project")
                    assert result is True

    def test_returns_false_on_failure(self):
        """Verify function returns False on failed deployment"""
        with tempfile.TemporaryDirectory() as tmpdir:
            src_file = os.path.join(tmpdir, "test.html")
            with open(src_file, 'w') as f:
                f.write("<html></html>")

            with patch('deploy_domains.PAGES_DIR', tmpdir):
                with patch('subprocess.run') as mock_run:
                    mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="Error occurred")

                    result = deploy_domain("test.html", "test-project")
                    assert result is False

    def test_handles_missing_source_file(self):
        """Graceful handling when HTML file doesn't exist"""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('deploy_domains.PAGES_DIR', tmpdir):
                with patch('subprocess.run') as mock_run:
                    # Should raise exception or return False
                    result = deploy_domain("nonexistent.html", "test-project")
                    assert result is False
                    # subprocess.run should not be called
                    mock_run.assert_not_called()

    def test_handles_subprocess_timeout(self):
        """Proper error handling for deployment timeouts"""
        import subprocess

        with tempfile.TemporaryDirectory() as tmpdir:
            src_file = os.path.join(tmpdir, "test.html")
            with open(src_file, 'w') as f:
                f.write("<html></html>")

            with patch('deploy_domains.PAGES_DIR', tmpdir):
                with patch('subprocess.run') as mock_run:
                    mock_run.side_effect = subprocess.TimeoutExpired(cmd="wrangler", timeout=120)

                    result = deploy_domain("test.html", "test-project")
                    assert result is False

    def test_cleans_up_temp_directory_on_success(self):
        """Verify temp directory is removed after successful deployment"""
        with tempfile.TemporaryDirectory() as tmpdir:
            src_file = os.path.join(tmpdir, "test.html")
            with open(src_file, 'w') as f:
                f.write("<html></html>")

            captured_temp_dir = None

            def capture_temp_dir(*args, **kwargs):
                nonlocal captured_temp_dir
                captured_temp_dir = kwargs.get('cwd')
                return MagicMock(returncode=0, stdout="", stderr="")

            with patch('deploy_domains.PAGES_DIR', tmpdir):
                with patch('subprocess.run', side_effect=capture_temp_dir):
                    deploy_domain("test.html", "test-project")

            # Temp directory should be cleaned up
            if captured_temp_dir:
                assert not os.path.exists(captured_temp_dir), "Temp directory not cleaned up"

    def test_cleans_up_temp_directory_on_failure(self):
        """Verify temp directory is removed even on deployment failure"""
        with tempfile.TemporaryDirectory() as tmpdir:
            src_file = os.path.join(tmpdir, "test.html")
            with open(src_file, 'w') as f:
                f.write("<html></html>")

            captured_temp_dir = None

            def capture_temp_dir(*args, **kwargs):
                nonlocal captured_temp_dir
                captured_temp_dir = kwargs.get('cwd')
                return MagicMock(returncode=1, stdout="", stderr="Error")

            with patch('deploy_domains.PAGES_DIR', tmpdir):
                with patch('subprocess.run', side_effect=capture_temp_dir):
                    deploy_domain("test.html", "test-project")

            # Temp directory should still be cleaned up
            if captured_temp_dir:
                assert not os.path.exists(captured_temp_dir), "Temp directory not cleaned up after failure"

    def test_wrangler_command_structure(self):
        """Verify wrangler is called with correct arguments"""
        with tempfile.TemporaryDirectory() as tmpdir:
            src_file = os.path.join(tmpdir, "test.html")
            with open(src_file, 'w') as f:
                f.write("<html></html>")

            with patch('deploy_domains.PAGES_DIR', tmpdir):
                with patch('subprocess.run') as mock_run:
                    mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

                    deploy_domain("test.html", "my-project")

                    call_args = mock_run.call_args[0][0]
                    assert call_args[0] == "wrangler"
                    assert "pages" in call_args
                    assert "deploy" in call_args
                    assert "--project-name" in call_args
                    assert "my-project" in call_args

    def test_extracts_deployment_url(self, capsys):
        """Verify deployment URL is extracted and printed"""
        with tempfile.TemporaryDirectory() as tmpdir:
            src_file = os.path.join(tmpdir, "test.html")
            with open(src_file, 'w') as f:
                f.write("<html></html>")

            with patch('deploy_domains.PAGES_DIR', tmpdir):
                with patch('subprocess.run') as mock_run:
                    mock_run.return_value = MagicMock(
                        returncode=0,
                        stdout="Deployment complete! https://test-abc123.pages.dev deployed",
                        stderr=""
                    )

                    deploy_domain("test.html", "test-project")

                    captured = capsys.readouterr()
                    # Should contain success message
                    assert "Successfully deployed" in captured.out


class TestPagesDir:
    """Tests for the PAGES_DIR constant"""

    def test_pages_dir_is_absolute_path(self):
        """PAGES_DIR should be an absolute path"""
        assert os.path.isabs(PAGES_DIR), "PAGES_DIR should be an absolute path"

    def test_pages_dir_ends_with_pages(self):
        """PAGES_DIR should end with 'pages'"""
        assert PAGES_DIR.endswith('pages'), "PAGES_DIR should end with 'pages'"
