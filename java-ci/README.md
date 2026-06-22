# common-ci

This repository exposes a reusable GitHub Actions workflow for Java projects.

Usage (caller repository must supply required inputs):
```yaml
jobs:
  call-common-ci:
    uses: your-org/your-repo/.github/workflows/common-java-ci.yml@main
    with:
      java-version: '17'            # REQUIRED
      image-name: 'ghcr.io/org/app' # REQUIRED (used for docker image tagging)
      enable-security: true         # REQUIRED (true/false)
      enable-review: true           # REQUIRED (true/false)
      enable-test-generation: true  # REQUIRED (true/false)
      enable-docker: false          # REQUIRED (true/false)
      enable-autofix: false         # REQUIRED (true/false) - enables optional auto-fix steps
      build-tool: 'maven'           # optional, defaults to 'maven'
      maven-goals: 'verify'         # optional
    secrets:
      GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}