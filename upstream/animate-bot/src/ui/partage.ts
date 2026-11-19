import {
  COLOR_BY_ID,
  SHAPE_BY_ID,
  type ColorId,
  type ShapeId
} from '@/bot/skins'
import {
  EXPRESSION_BY_ID,
  type ExpressionId
} from '@/bot/expressions'

export interface ReglagesPartages {
  shape: ShapeId
  color: ColorId
  expression: ExpressionId
}

/**
 * Relit les reglages presents dans un fragment partage.
 *
 * Chaque valeur est gardee separement : un lien ancien dont une seule valeur
 * n'existe plus peut encore restaurer les deux autres sans injecter un id
 * inconnu dans le moteur.
 */
export function litReglagesPartages(fragment: string): Partial<ReglagesPartages> | null {
  const params = new URLSearchParams(fragment.replace(/^#/, ''))
  const forme = params.get('forme')
  const couleur = params.get('couleur')
  const expression = params.get('expression')
  const reglages: Partial<ReglagesPartages> = {}

  if (forme && SHAPE_BY_ID.has(forme)) reglages.shape = forme as ShapeId
  if (couleur && COLOR_BY_ID.has(couleur)) reglages.color = couleur as ColorId
  if (expression && EXPRESSION_BY_ID.has(expression)) {
    reglages.expression = expression as ExpressionId
  }

  return Object.keys(reglages).length ? reglages : null
}

/** Construit un lien autonome, sans conserver l'etat du lecteur dans le fragment. */
export function lienPartage(base: string, reglages: ReglagesPartages): string {
  const url = new URL(base)
  const params = new URLSearchParams()
  params.set('forme', reglages.shape)
  params.set('couleur', reglages.color)
  params.set('expression', reglages.expression)
  url.hash = params.toString()
  return url.toString()
}
