import { describe, expect, it } from 'vitest'
import { lienPartage, litReglagesPartages } from './partage'

describe('lien de partage', () => {
  it('restaure une personnalisation complete', () => {
    expect(
      litReglagesPartages('#forme=capsule&couleur=bleu&expression=heureux')
    ).toEqual({
      shape: 'capsule',
      color: 'bleu',
      expression: 'heureux'
    })
  })

  it('ignore les valeurs inconnues sans perdre les valeurs valides', () => {
    expect(
      litReglagesPartages('#forme=inconnue&couleur=rouge&expression=inconnue')
    ).toEqual({
      color: 'rouge'
    })
    expect(litReglagesPartages('#forme=inconnue')).toBeNull()
  })

  it('remplace le fragment du lecteur par les reglages partages', () => {
    expect(
      lienPartage('https://animate-bot.example/demo?source=test#etat=orbit&stop', {
        shape: 'nuage',
        color: 'violet',
        expression: 'curieux'
      })
    ).toBe(
      'https://animate-bot.example/demo?source=test#forme=nuage&couleur=violet&expression=curieux'
    )
  })
})
