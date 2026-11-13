# x-material-library 数据目录

此目录用于在 DADA 仓库中跟踪 x-material-library 的目录数据。`items.js` 是网站读取的 `window.ITEMS` 清单，`items.json` 是同一份清单的可读 JSON；本批保留网站 basePath `/s/rjqagsc0hcqp/`，没有改动站点 UI。

## 当前 canonical 快照（2026-11-13）

- 当前清单由 131 条保留素材记录和 6 条仅代码预览记录组成，共 137 条、137 个唯一 ID；PR #85 按批准名单删除的 114 个素材 ID 仍全部缺席，未恢复原记录或其媒体。
- 62 个现有 `effects/<slug>/code/index.html` 均有且仅有一个代码状态记录映射：56 条映射到保留素材记录；其余 6 条为代码专用预览记录，其中 4 条使用 `effect-<slug>` 合成 ID，`pro-threads` 和 `voice-orbs` 沿用各自效果 README 中已有的素材 ID。它们均标记为 `code_only_preview`，不恢复被删除条目的来源 ID 或素材数据。
- 预览路径根因：原有 14 条代码状态记录仍指向 `assets/<id>/code/index.html` 旧路径。当前线上这些 URL 返回 HTTP 200，但它们是 staging 中的旧副本，并非仓库 canonical 输出；例如 `sonia-aurora-loader` 线上旧副本 SHA-256 为 `8f1778995c1dc9c9c5cd572e99b2188f21afd9d7fd7ac28d4841a945c04d7c83`，仓库 `effects/sonia-aurora-loader/code/index.html` 为 `a7a1c4eb17dd8fe1c414ab0f9b7a012fe25cb67129767c839d86ab005442620d`。canonical 实现位于 `effects/<slug>/code/`；该效果树当前尚未发布，线上 `/effects/` canonical 路径中的 `sonia-aurora-loader`、`pro-threads`、`voice-orbs`、`light-progress-bar`、`jh3yy-flip-to-tip` 页面返回 404。此 PR 将 62 条代码状态记录的 `code` 值统一改为对应 `effects/<slug>/code/index.html`（iframe 直接读取该字段）；此次仅修正元数据，不组装或部署 staging，需由后续完整站点树发布使这些预览上线。
- 线上 `items.js` 返回 131 条；某个浏览器 UI 显示 129 条，是 `index.html` 按本地 `localStorage` 的 `dada-library-edits` / `store.hidden` 隐藏了其中两条。未读取或修改该浏览器存储，具体 ID 未核验；这不改变 canonical 清单的记录数。
- `items.js` 与 `items.json` 保持语义一致；没有改动站点 UI、布局、功能、basePath `/s/rjqagsc0hcqp/` 或任何效果实现文件。
- 62 个预览目录共 63 个代码文件（`voice-orbs` 含一个附加文件）。部署组装时，这些文件会加入现有 456 文件站点 staging；在替换旧代码路径副本、清理未引用资源之前为 519 个文件。本次不修改部署 staging。
- 历史导入 manifest 继续记录导入当时的事实，不代表当前 canonical 清单；下文的 11/10–11/12 数量是当时批次的历史快照。

## 2026-11-10/12 数据增量

- 线上基线：187 条、187 个唯一 ID。
- 原批次新增：44 条（11 月 10 日 24 条，11 月 11 日 20 条）；本次再追加主人指定的收藏 1 条，总新增 45 条。
- 当前快照：232 条、232 个唯一 ID（187 条线上基线 + 原有 44 条 + 本次 1 条）；187 条线上基线逐条不变。
- 原批次新增媒体：43 个 `assets/<id>/` 目录，共 156 个文件。对这些新增资产引用做了检查，并从 35 条记录中移除了本包未提供的 `gif_local` / `full_video_local` 字段（70 个悬空路径）。本次收藏保留 X 原帖 URL，记录原帖含 2 张图片和 2 段视频；未复制媒体，许可未核验。
- 明细见 `import-manifest-20261110-11.json`。

## 2026-11-12 数据增量

- 来源包：`x-material-library-newitems-20261112.zip`，MD5 `bde95699f710a32f2c5db68877236db5`（原包 14 条：新增 13 个唯一 ID，更新已有 x6sense 条目 `2120533831136751633` 1 条）。
- 合并后清单：245 条、245 个唯一 ID；在原 232 条快照中仅更新上述 x6sense 记录，其余 231 条不变，既有 187 条线上基线也保留。
- 媒体：新增 14 个 `assets/<id>/` 目录、55 个文件；包括 x6sense 已有记录的 6 个本地媒体文件。保留原帖 URL、作者、`added_at` 和 `license_status: not_verified`，只补充包内媒体及描述/分类/标签/计数等元数据。
- 14 条记录的本地媒体引用全部核验，缺失引用为 0。删除 27 个指向包内不存在文件的可选引用（13 个 `gif_local`、13 个 `full_video_local`、1 个 `extra_videos_local`），受影响 ID：`2120345620116308381`、`2120411877985681812`、`2120518489022595177`、`2120533299269619933`、`2120533831136751633`、`2120553374286594292`、`2120607242860757135`、`2120607704142037228`、`2120626950092083630`、`2120651303156130285`、`2120752319243723236`、`2120809570344050705`、`2120841809559535629`。
- 素材授权均未核验；未推断授权、真实交互或代码。明细见 `import-manifest-20261112.json`。

## 部署边界（PR #84 历史说明，2026-11-12）

本节描述的是 2026-11-12 的 PR #84（11/10–11/12 导入批次）当时的部署边界，不代表当前 PR #85。PR #84 只包含 `site-data/x-material-library/` 数据清单、导入 manifest 与新增素材，不是完整静态站点包或整站覆盖。目录内的 14 个新增素材目录（含 x6sense 原有条目的媒体补充）应叠加到完整站点已有资源树；不得将本目录单独作为部署根目录，也不得删除或覆盖其余站点资源。既有 187 条线上基线及 DADA 站点 UI、布局、功能和 basePath `/s/rjqagsc0hcqp/` 必须保留。PR #84 不包含 UI/效果代码修改，也不包含部署操作；应在独立审核及 CI 门禁通过后再决定发布。

PR #85 是按批准名单对现有清单做删减（见上文「当前 canonical 快照」），不复用本节所述的 14 个新增目录，也不包含 UI/效果代码修改与部署操作。
