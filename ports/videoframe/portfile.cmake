

vcpkg_from_git(
    OUT_SOURCE_PATH SOURCE_PATH
    URL git@bitbucket.org:id4tv/videoframe.git
    REF b6d9d5aeb4aac66cc43b809cf23f72de21933c18
    HEAD_REF master
)

vcpkg_configure_cmake(
  SOURCE_PATH "${SOURCE_PATH}"
  PREFER_NINJA
)
vcpkg_install_cmake()
vcpkg_fixup_cmake_targets()

file(REMOVE_RECURSE "${CURRENT_PACKAGES_DIR}/debug/include")

file(
  INSTALL "${SOURCE_PATH}/LICENSE"
  DESTINATION "${CURRENT_PACKAGES_DIR}/share/${PORT}"
  RENAME copyright)