class MergeDependabot < Formula
  desc "Merge green Dependabot PRs and sync all repos in ~/Documents/Github"
  homepage "https://github.com/SiavoshZarrasvand/homebrew-merge-dependabot"
  url "https://github.com/SiavoshZarrasvand/homebrew-merge-dependabot/archive/refs/tags/v1.0.0.tar.gz"
  sha256 "3de2749a2d02aa83b217d061bab8968fda402b7b2585a6c90bdf4cb977d148f3"
  license "MIT"
  version "1.0.0"

  depends_on "gh"

  def install
    chmod 0755, "merge-dependabot"
    bin.install "merge-dependabot"
  end

  test do
    output = shell_output("#{bin}/merge-dependabot --version")
    assert_match "1.0.0", output
  end
end
